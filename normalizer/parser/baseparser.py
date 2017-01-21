#!/usr/bin/python
# -*- coding: utf8 -*-
import logging

import requests


class BaseParser(object):
    def __int__(self):
        self._logger = logging.getLogger(__name__)
        self.domain = None

    # Tải nội dung web
    def get_html(self, url, timeout=15):
        try:
            response = requests.get(url=url, timeout=timeout)
            if response.status_code == requests.codes.ok:
                return response.content.decode('UTF-8')
        except Exception as e:
            self._logger.exception(e)
        return None

    def get_source(self, content):
        pass

    def get_title(self, content):
        pass

    def get_author(self, content):
        pass

    def parse(self, url, timeout=15):
        html = self.get_html(url, timeout=timeout)
        if html is None:
            return None


        '''
        Format:
+ Mỗi paragraph nằm trong thẻ <p></p>
+ Hình nằm trong thẻ <img...>
    + Alt: Title của bài
    + Src: link ảnh
    Caption: <p class="caption"></p> và liền sau ảnh
+ Video: <video></video>
<video width="375" height="280">
    <source src="movie.mp4" type="video/mp4">
    <source src="movie.ogg" type="video/ogg">
</video>

<img alt="" src="">



        normalize:
        get_title
        get_description
        get_content
        remove_htmltag and content
        get_tag -> loop -> process image, video, text | loop over child
        clear html tag
        escape_html
        image
        video
        content
        '''

        print(html)
        return {
            "SourcePage": "",
            "Title": "",
            "Url": "",
            "Author": "",
            "Thumbnail": "",
            "Tag": "",
            "ShortIntro": "",
            "PublishDate": "",
            "MetaDescription": "",
            "MetaKeywords": "",
            "CrawledDate": "",
            "Content": "",
            "Plain_Content": "",
        }
