import os
import sys
import requests
import time
import json
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Optional
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import settings


def parse_catalog_page(url: str) -> List[Dict[str, Any]]:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    products = []

    product_blocks = soup.find_all('div', class_='new-product')
    for block in product_blocks:
        link_tag = block.find('a', class_='product', href=True)
        if not link_tag:
            continue

        product_url = "https://www." + link_tag['href'].strip()
        title_tag = block.find('div', class_='title')
        price_tag = block.find('span', class_='price')
        description_tag = block.find('div', class_='description')
        image_tag = block.find('img', class_='image')

        product = {
            'url': product_url,
            'title': title_tag.text.strip() if title_tag else None,
            'price': price_tag.text.strip() if price_tag else None,
            'short_description': description_tag.text.strip() if description_tag else None,
            'image': image_tag['src'] if image_tag else None
        }

        try:
            product.update(parse_product_page(product_url))
        except Exception as e:
            logger.warning(f"{product_url}, ошибка: {e}")

        products.append(product)
        time.sleep(2)

    return products


def parse_product_page(url: str) -> Dict[str, Any]:
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')

    result = {}

    description_block = soup.find('div', id='produce-parts-description-content')
    full_description = description_block.get_text(strip=True, separator='\n') if description_block else None

    attributes = {}
    attribute_rows = soup.find_all('div', class_='row')
    for row in attribute_rows:
        cells = row.find_all('div')
        if len(cells) >= 2:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            attributes[key] = value

    result['full_description'] = full_description
    result['attributes'] = attributes

    return result


def split_text_into_chunks(text: str, metadata: Dict[str, Any]) -> List[Any]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.MAX_CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.create_documents(texts=[text], metadatas=[metadata])
    return chunks


def generate_chroma_db() -> Optional[Chroma]:
    try:
        os.makedirs(settings.CHROMA_PATH, exist_ok=True)

        catalog_url = "https://www."
        products = parse_catalog_page(catalog_url)

        if not products:
            logger.warning("Нет товаров")
            return None

        embeddings = HuggingFaceEmbeddings(
            model_name=settings.LM_MODEL_NAME,
            model_kwargs={"device": "cuda" if False else "cpu"},  
            encode_kwargs={"normalize_embeddings": True},
        )

        all_chunks = []
        for i, item in enumerate(products):
            content = ""

            if item.get("title"):
                content += f"Название: {item['title']}\n"
            if item.get("price"):
                content += f"Цена: {item['price']}\n"
            if item.get("short_description"):
                content += f"Краткое описание: {item['short_description']}\n"
            if item.get("full_description"):
                content += f"Полное описание: {item['full_description']}\n"
            if item.get("attributes"):
                content += "Характеристики:\n"
                for k, v in item["attributes"].items():
                    content += f"- {k}: {v}\n"

            metadata = {
                "title": item.get("title") or "",
                "price": item.get("price") or "",
                "url": item.get("url") or "",
                "short_description": item.get("short_description") or "",
                "full_description": item.get("full_description") or "",
                "attributes": json.dumps(item.get("attributes"), ensure_ascii=False) or "",
                "image": item.get("image") or ""
            }

            chunks = split_text_into_chunks(content, metadata)
            all_chunks.extend(chunks)
            logger.info(f"Товар {i+1}/{len(products)} разбит на {len(chunks)} чанков")

        ids = [f"doc_{i}" for i in range(len(all_chunks))]

        texts = [chunk.page_content for chunk in all_chunks]
        metadatas = [chunk.metadata for chunk in all_chunks]

        chroma_db = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            ids=ids,
            metadatas=metadatas,
            persist_directory=settings.CHROMA_PATH,
            collection_name=settings.COLLECTION_NAME,
            collection_metadata={"hnsw:space": "cosine"},
        )

        logger.info(
            f"Добавлено {len(all_chunks)} чанков из {len(products)} товаров"
        )
        return chroma_db

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise


if __name__ == "__main__":
    generate_chroma_db()
