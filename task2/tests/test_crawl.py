import aiohttp
import pytest

from solution.main import crawl


MOCK_HTML_SINGLE_PAGE = """
<div id="mw-pages">
  <div class="mw-category-group">
    <h3>А</h3>
    <ul>
      <li><a href="/wiki/Антилопа">Антилопа</a></li>
      <li><a href="/wiki/Акула">Акула</a></li>
    </ul>
  </div>
</div>
"""


MOCK_HTML_WITH_NEXT = """
<div id="mw-pages">
  <div class="mw-category-group">
    <h3>А</h3>
    <ul>
      <li><a href="/wiki/Аист">Аист</a></li>
    </ul>
  </div>
  <a href="/w/index.php?title=Категория:Животные_по_алфавиту&from=А&page=2">Следующая страница</a>
</div>
"""


MOCK_HTML_SECOND_PAGE = """
<div id="mw-pages">
  <div class="mw-category-group">
    <h3>А</h3>
    <ul>
      <li><a href="/wiki/Архар">Архар</a></li>
    </ul>
  </div>
</div>
"""


@pytest.mark.asyncio
async def test_crawl_single_page(monkeypatch):
    async def mock_fetch(session, url):
        return MOCK_HTML_SINGLE_PAGE

    monkeypatch.setattr("solution.main.fetch", mock_fetch)

    async with aiohttp.ClientSession() as session:
        result = await crawl(session, "А")

    assert result == 2


@pytest.mark.asyncio
async def test_crawl_multiple_pages(monkeypatch):
    pages = [MOCK_HTML_WITH_NEXT, MOCK_HTML_SECOND_PAGE]

    async def mock_fetch(session, url):
        return pages.pop(0)

    monkeypatch.setattr("solution.main.fetch", mock_fetch)

    async with aiohttp.ClientSession() as session:
        result = await crawl(session, "А")

    assert result == 2
