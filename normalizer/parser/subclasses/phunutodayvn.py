#!/usr/bin/python
# -*- coding: utf8 -*-
import bleach
from bs4 import Tag, NavigableString

from normalizer import *


class PhuNuTodayVnParser(BaseParser):
    _video_url_regex = regex.compile(r'file\s*:\s*"([^"]+)"', regex.IGNORECASE)

    def __init__(self):
        super().__init__()
        self._domain = 'phunutoday.vn'

    def get_direct_video(self, url, timeout=15):
        if self._domain not in url:
            return None

        raw_html = self.get_html(url=url, timeout=timeout, allow_redirects=False)
        if raw_html is None:
            return None

        video_url = self._video_url_regex.search(raw_html)
        if video_url is None:
            return None

        video_url = video_url.group(1)
        mime_type = self.get_mime_from_url(video_url)
        if mime_type is None:
            return None

        return video_url, mime_type

    def get_main_content(self, html, title):
        div_tag = html.find('div', id='content_detail')
        if div_tag is None:
            return None

        # Remove ads
        trash_items = div_tag.find_all(class_=regex.compile(r'list_suggest_link|list_suggest_desk|adv'))
        for trash_item in trash_items:
            trash_item.decompose()

        # Handle videos
        video_tags = div_tag.find_all('iframe', class_='exp_video')
        for video_tag in video_tags:
            video_src = video_tag.get('src')

            direct_video = self.get_direct_video(video_src)
            if direct_video is None:
                video_tag.decompose()  # Remove if do not exist
            else:
                video_url, mime_type = direct_video

                new_source_tag = html.new_tag('source')
                new_source_tag['src'] = video_url
                new_source_tag['type'] = mime_type

                new_video_tag = html.new_tag('video')
                new_video_tag['width'] = '375'
                new_video_tag['height'] = '280'
                new_video_tag.append(new_source_tag)

                video_tag.replace_with(new_video_tag)

        # Handle image
        figures = div_tag.find_all('figure')
        for figure in figures:
            caption_image = figure.find('figcaption')

            image_tag = html.new_tag('img')
            image_tag['src'] = self.get_absolute_url(figure.img.get('src'))
            image_tag['alt'] = title if figure.img.get('alt') is None else figure.img.get('alt')

            figure.replace_with(image_tag)

            if caption_image is not None:
                caption_tag = html.new_tag('cap')
                caption_tag.append(self.normalize_string(caption_image.get_text()))
                image_tag.insert_after(caption_tag)

        # Handle content
        div_tag.name = 'content'

        attrs = {
            'video': ['width', 'height'],
            'source': ['src', 'type'],
            'img': ['src', 'alt']
        }
        content_tag = bleach.clean(div_tag, tags=['content', 'video', 'source', 'img', 'cap', 'p', 'div', 'br'],
                                   attributes=attrs, strip=True)
        content_tag = BeautifulSoup(content_tag, 'html5lib')
        content_tag = content_tag.content

        block_tags = content_tag.find_all(['div', 'p', 'video', 'img', 'cap'])
        for block_tag in block_tags:
            block_tag.insert_before(BeautifulSoup('<br>', 'xml').br)
            block_tag.insert_after(BeautifulSoup('<br>', 'xml').br)
            if block_tag.name not in ['video', 'img', 'cap']:
                block_tag.unwrap()

        # Normalize
        paragraphs = []
        for child in content_tag.children:
            if isinstance(child, Tag):
                if child.name in ['img', 'video']:
                    paragraphs.append(str(child))
                elif 'cap' in child.name:
                    paragraphs.append('<p class="caption">%s</p>' % self.normalize_string(str(child.cap)))
            elif isinstance(child, NavigableString):
                normalized_string = self.normalize_string(child.string)
                if len(normalized_string) > 0:
                    paragraphs.append('<p>%s</p>' % normalized_string)

        paragraphs = ''.join(paragraphs)
        paragraphs = BeautifulSoup(paragraphs, 'html5lib').body
        return paragraphs

    def get_tags(self, html, main_content):
        return self.get_meta_keywords(html=html)

    def get_summary(self, html, main_content):
        return self.get_meta_description(html=html)

    def get_content(self, main_content):
        if main_content is None:
            return None
        return regex.sub(r'<body>|<\/body>|<\/source>', '', str(main_content))

    def get_author(self, html, main_content):
        div_tag = html.find('div', class_='tags')
        if div_tag is None:
            return None
        div_tag = div_tag.find_next('div')
        if div_tag is None:
            return None
        return self.normalize_string(div_tag.p.text)

    def get_thumbnail(self, html, main_content):
        img_tag = main_content.find('img')
        if img_tag is None:
            return None
        return img_tag.get('src')

    def get_publish_date(self, html, main_content):
        time_tag = html.find('time', class_='fl')
        if time_tag is None:
            return None
        time_string = regex.sub(r',[^\d]+', ' ', time_tag.span.text.strip())
        return datetime.strptime(time_string, '%H:%M %d/%m/%Y').strftime('%Y-%m-%d %H:%M:%S')
