const newsButton = document.getElementById('more-news');
const olderNews = [...document.querySelectorAll('.older-news')];
if (newsButton && olderNews.length) {
  newsButton.addEventListener('click', () => {
    const expand = newsButton.getAttribute('aria-expanded') !== 'true';
    olderNews.forEach(item => { item.hidden = !expand; });
    newsButton.setAttribute('aria-expanded', String(expand));
    newsButton.textContent = expand ? 'Show fewer updates −' : 'Show earlier updates +';
    (expand ? olderNews[0] : document.getElementById('news')).scrollIntoView({block: 'start'});
  });
}
