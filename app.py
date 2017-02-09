#!/usr/bin/python
# -*- coding: utf8 -*-

import os

from bs4 import NavigableString

os.environ['PAFY_BACKEND'] = 'internal'

from crawler import *
from normalizer import *
from helpers import *


def _combine_span_tags(span_tag, block_classes=None):
    if span_tag is None or isinstance(span_tag, NavigableString) or span_tag.name != 'span':
        return None

    # Wrap lại bằng div để tránh rời rạc
    span_tag.wrap(create_html_tag('div'))

    parent_span_tag = span_tag.parent

    if block_classes is None:
        block_classes = []

    span_classes = span_tag.get('class')
    if span_classes is None:
        span_classes = []

    span_classes.extend(block_classes)

    s = [(span_tag, list(set(span_classes)))]

    while len(s) > 0:
        tag, classes = s.pop()

        current_tag = tag

        # Lặp qua từng node con
        children = list(tag.children)

        if len(children) > 0:
            temp_tag = create_html_tag('span', attrs={'class': classes} if len(classes) > 0 else {})

            for child_tag in children:
                if isinstance(child_tag, NavigableString):
                    temp_tag.append(child_tag.extract())
                else:
                    # Bổ sung thẻ span vào cây nếu có dữ liệu, chỉ nhận thẻ span chứa nội dung có ý nghĩa
                    if len(temp_tag.contents) > 0:
                        # Chèn vào sau thẻ cha
                        current_tag.insert_after(temp_tag)
                        if not is_valid_string(temp_tag.text, r'\s+'):
                            temp_tag.unwrap()

                        current_tag = current_tag.next_sibling
                        temp_tag = create_html_tag('span', attrs={'class': classes} if len(classes) > 0 else {})

                    if child_tag.name == 'br':
                        current_tag.insert_after(child_tag.extract())
                        current_tag = current_tag.next_sibling
                    else:
                        # Lấy thẻ span con ra để khi thẻ cha bị xóa thì không bị xóa theo
                        child_span_tag = child_tag.extract()

                        span_classes = child_tag.get('class')
                        if span_classes is None:
                            span_classes = []

                        span_classes.extend(classes)

                        if len(child_span_tag.contents) > 0:
                            current_tag.insert_after(child_span_tag)
                            current_tag = current_tag.next_sibling
                            s.append((child_span_tag, list(set(span_classes))))
                        else:
                            child_span_tag.decompose()

            # Trường hợp không có tag để đóng lại
            if len(temp_tag.contents) > 0:
                # Chèn vào sau thẻ cha
                current_tag.insert_after(temp_tag)
                if not is_valid_string(temp_tag.text, r'\s+'):
                    temp_tag.unwrap()

        # Xóa thẻ cha vì con của nó đã được đem lên cùng cấp nằm ở phía sau
        tag.decompose()

    return parent_span_tag


def _combine_span_sibling_tags(div_tag):
    if div_tag is None or isinstance(div_tag, NavigableString) or div_tag.name != 'div':
        return None

    children = list(div_tag.children)
    children_size = len(children)

    i = 0
    while i < children_size - 1:
        child_tag = children[i]

        if child_tag.name == 'span':

            j = i + 1
            while j < children_size:
                next_sibling = children[j]

                if isinstance(next_sibling, NavigableString):
                    if is_valid_string(str(next_sibling), r'\s+'):
                        break
                    else:
                        # Gộp thẻ span và text gồm các khoảng trắng
                        child_tag.append(next_sibling.extract())
                        i = j
                else:
                    if next_sibling.name == 'span':
                        # Xử lí gộp hai span kề nhau có chung class
                        child_classes = child_tag.get('class')
                        if child_classes is None:
                            child_classes = []

                        next_sibling_classes = next_sibling.get('class')
                        if next_sibling_classes is None:
                            next_sibling_classes = []

                        if set(child_classes) == set(next_sibling_classes):
                            # Gộp 2 thẻ span
                            child_tag.append(next_sibling.extract())
                            next_sibling.unwrap()
                            i = j
                        else:
                            break
                    else:
                        break
                j += 1
        i += 1

    # Nếu thẻ div chỉ chứa 1 span thì gộp class của span đó với div bao bên ngoài
    #print(div_tag.find_all(True))
    #div_tag.string -> None


def _combine_div_tags(parent_tag):
    if parent_tag is None or isinstance(parent_tag, NavigableString) or parent_tag.name != 'div':
        return None

    # Clone thẻ div để khi unwrap vẫn không bị mất.
    parent_tag.wrap(create_html_tag('div', attrs=parent_tag.attrs))

    classes = parent_tag.get('class')
    s = [(parent_tag, [] if classes is None else classes)]

    while len(s) > 0:
        tag, classes = s.pop()

        # Lặp qua từng node con
        children = list(tag.children)
        children_size = len(children)

        if children_size > 0:
            temp_tag = create_html_tag('div', attrs={'class': classes} if len(classes) > 0 else {})

            i = 0
            while i < children_size:
                child_tag = children[i]

                if isinstance(child_tag, NavigableString):
                    temp_tag.append(child_tag.extract())
                elif child_tag.name == 'span':
                    span_tags = _combine_span_tags(span_tag=child_tag, block_classes=temp_tag.attrs.get('class'))

                    contents = list(span_tags.children)
                    for child in contents:
                        if child.name == 'br':
                            if len(temp_tag.contents) > 0 and is_valid_string(temp_tag.text, r'\s+'):
                                span_tags.insert_before(temp_tag)

                                # Gộp các span anh em có chung class
                                _combine_span_sibling_tags(div_tag=temp_tag)

                                temp_tag = create_html_tag('div', attrs={'class': classes} if len(classes) > 0 else {})
                        else:
                            temp_tag.append(child.extract())

                    span_tags.decompose()
                else:
                    # Bổ sung thẻ div vào cây nếu có dữ liệu, chỉ nhận thẻ div chứa nội dung có ý nghĩa
                    if len(temp_tag.contents) > 0 and is_valid_string(temp_tag.text, r'\s+'):
                        child_tag.insert_before(temp_tag)

                        # Gộp các span anh em có chung class
                        _combine_span_sibling_tags(div_tag=temp_tag)

                        temp_tag = create_html_tag('div', attrs={'class': classes} if len(classes) > 0 else {})

                    if child_tag.name == 'div':
                        # Thêm vào stack nếu là div
                        child_classes = child_tag.get('class')
                        if child_classes is None:
                            child_classes = []
                        child_classes.extend(classes)
                        if len(child_tag.contents) > 0 and (
                                    is_valid_string(child_tag.text, r'\s+') or child_tag.find(
                                    ['video', 'img']) is not None):
                            s.append((child_tag, list(set(child_classes))))
                        else:
                            child_tag.decompose()
                    else:
                        if child_tag.name not in ['video', 'img']:
                            child_tag.decompose()

                i += 1

            # Trường hợp không có tag để đóng lại, chỉ nhận thẻ div chứa nội dung có ý nghĩa
            if len(temp_tag.contents) > 0 and is_valid_string(temp_tag.text, r'\s+'):
                # Đã duyệt qua tất cả thẻ con nên chỉ cần append để vào vị trí cuối
                tag.append(temp_tag)

                # Gộp các span anh em có chung class
                _combine_span_sibling_tags(div_tag=temp_tag)

            # Xóa thẻ div ngoài cùng nhưng vẫn giữ các thẻ con bên trong nó
            tag.unwrap()
        else:
            # Xóa thẻ div nếu nó không có thẻ con
            tag.decompose()


def main():
    crawler = Crawler()
    normalizer = Normalizer()

    url = ''
    crawler.crawl(url=url)

    return
    d = '''
    <div>
            <div>Đến nay, cuộc CMCN lần thứ 4 (4.0) sẽ hình thành những công nghệ giúp xóa nhòa ranh giới giữa các lĩnh vực vật lý, số hóa và sinh học cả trong đời sống, sản xuất, cũng như trong lĩnh vực giáo dục đào tạo và giáo dục nghề nghiệp (GDNN). Từ những tác động đó, cần có những giải pháp nhằm nâng cao chất lượng đào tạo nghề nghiệp, đáp ứng yêu cầu của nền kinh tế sáng tạo và hội nhập...</div><div><span class="bold">Những vấn đề đặt ra đối với GDNN</span></div><div>Trong cuộc cách mạng công nghiệp 4.0, thị trường lao động (TTLĐ) sẽ bị thách thức nghiêm trọng giữa chất lượng cung và cầu lao động cũng như cơ cấu lao động. Khi tự động hóa thay thế con người trong nhiều lĩnh vực của nền kinh tế, người lao động chắc chắn sẽ phải thích ứng nhanh với sự thay đổi của sản xuất nếu không sẽ bị dư thừa hay thất  nghiệp.</div><div>Theo dự báo, trong một số lĩnh vực, với sự xuất hiện của robot, số lượng nhân viên sẽ giảm đi 1/10 so với hiện nay, như vậy, 9/10 nhân lực còn lại sẽ phải chuyển nghề hoặc thất nghiệp. Cuối năm 2015, Ngân hàng Anh Quốc đưa ra dự báo: sẽ có khoảng 95 triệu lao động truyền thống bị mất việc trong vòng 10-20 năm tới... Hàng loạt nghề nghiệp cũ sẽ mất đi, thị trường lao động tại quốc gia này cũng như quốc tế sẽ phân hóa mạnh mẽ giữa nhóm lao động có kỹ năng thấp và nhóm lao động có kỹ năng cao… Đặc biệt, cuộc cách mạng 4.0 không chỉ đe dọa việc làm của những lao động trình độ thấp mà ngay cả lao động có kỹ năng bậc trung (trung cấp, cao đẳng) cũng sẽ bị ảnh hưởng, nếu như họ không được trang bị những kỹ năng mới - kỹ năng sáng tạo cho nền kinh tế 4.0.</div><div><div class="center"><img src="http://media.ldxh.vn/480/2017/2/2/Giao-duc-nghe-nghiep-5.jpg"/></div><div class="center"><span class="italic">Trong cuộc cách mạng công nghiệp 4.0, thị trường lao động sẽ bị thách thức nghiêm trọng giữa chất lượng cung và cầu lao động và ảnh hưởng đến giáo dục nghề nghiệp</span></div></div><div>Những sự thay đổi này của sản xuất và cơ cấu nhân lực trong TTLĐ tương lai, đặt ra nhiều vấn đề đối với GDNN, đó là:</div><div><span class="bold"><span class="italic">Thứ nhất</span></span><span class="italic"></span> các cơ sở GDNN phải đổi mới mạnh mẽ từ hoạt động đào tạo đến quản trị nhà trường để tạo ra những “sản phẩm”- người lao động tương lai có năng lực làm việc trong môi trường sáng tạo và cạnh tranh… Trong khi cuộc cách mạng công nghiệp 4.0 đang và sẽ tác động mạnh mẽ đến TTLĐ thì các cơ sở GDNN nơi cung cấp nhân lực kỹ thuật chủ yếu cho nền kinh tế, vẫn đào tạo theo cách đã cũ. Học sinh, sinh viên với các kiến thức, kỹ năng đang được dạy trong nhà trường hiện nay còn chưa đáp ứng được yêu cầu của nền kinh tế 3.0 hiện tại, có thể hoàn toàn không hữu dụng với nền kinh tế 4.0 hoặc đang dễ dàng bị robot thay thế trong tương lai gần.</div><div><span class="bold"><span class="italic">Thứ hai</span></span><span class="italic">,</span> thay đổi các hoạt động đào tạo, nhất là phương thức và phương pháp đào tạo với sự ứng dụng mạnh mẽ của CNTT. Tuy nhiên, hiện nay các điều kiện đảm bảo cho sự thay đổi này vẫn còn hạn chế. Đa số các các cơ sở GDNN, sự đổi mới phương thức và phương pháp dạy và học còn khá chậm trễ; hạ tầng CNTT còn lạc hậu (ngoại trừ một số cơ sở được đầu tư  thành trường chất lượng cao) và không đồng bộ. Trong một số năm gần đây, trong khuôn khổ của chương trình MTQG, ngành Dạy nghề đã triển khai các hoạt động của dự án ứng dụng CNTT trong quản lý, hoạt động dạy và học nghề. Hệ thống cơ sở dữ liệu quốc gia về dạy nghề được thiết kế, xây dựng cho phép thu thập, xử lý, cập nhật, đồng bộ thông tin dữ liệu về dạy nghề trên toàn quốc và hỗ trợ công tác tìm kiếm, thống kê, báo cáo, phân tích dự báo phục vụ cho công tác điều hành, quản lý về dạy nghề từ Trung ương đến bộ, ngành, địa phương, CSDN trên phạm vi cả nước.  Tuy nhiên, kết quả của dự án còn hạn chế, do mới chỉ đầu tư lắp đặt hạ tầng đồng bộ cho 26 trường CĐN và đang triển khai thí điểm số hóa bài giảng, mô phỏng thực hành nghề để hình thành cơ sở dữ liệu bài giảng điện tử nhằm hiện đại hóa công tác dạy và học nghề...</div><div><span class="bold"><span class="italic">Thứ ba</span></span><span class="italic">,</span> đào tạo ảo, mô phỏng, số hóa bài giảng sẽ là xu hướng đào tạo nghề nghiệp trong tương lai. Điều này tác động đến bố trí cán bộ quản lý, phục vụ và đội ngũ giáo viên của các cơ sở GDNN. Đội ngũ này phải được chuyên nghiệp hóa và có khả năng sáng tạo cao, có phương pháp đào tạo hiện đại với sự ứng dụng mạnh mẽ của CNTT và điều này dẫn đến sự thay đổi về quy mô và cơ cấu giáo viên (cả về trình độ và kỹ năng.</div><div><span class="bold"><span class="italic">Thứ tư</span></span><span class="italic">,<span class="bold"> </span></span> chuyển đổi mạnh mẽ sang mô hình chỉ đào tạo “những gì thị trường cần” và hướng tới chỉ đào tạo “những gì thị trường sẽ cần”.Theo mô hình mới này, việc gắn kết giữa cơ sở GDNN với doanh nghiệp là yêu cầu được đặt ra; đồng thời, đẩy mạnh việc hình thành các cơ sở đào tạo trong doanh nghiệp để chia sẻ các nguồn lực chung: cơ sở vật chất, tài chính, nhân lực, quan trọng hơn là rút ngắn thời gian chuyển giao từ kiến thức, kỹ năng vào thực tiễn cuộc sống. Tuy nhiên, mối quan hệ gắn kết giữa nhà trường và doanh nghiệp; giữa đào tạo và sử dụng nhân lực qua đào tạo vẫn còn rất ‘lỏng lẻo, chưa trở thành “trách nhiệm xã hội” của các doanh nghiệp.</div><div><span class="bold"><span class="italic">Thứ năm</span></span><span class="italic">,</span> với sự xuất hiện ở những lớp học ảo, nghề ảo, chương trình ảo, và những yêu cầu của TTLĐ với những kỹ năng sáng tạo mới, đòi hỏi có sự quản lý chung để một mặt hướng tới sự đảm bảo “mặt bằng” chất lượng; mặt khác, đáp ứng nhu cầu đa dạng của nền kinh tế sáng tạo và cạnh tranh. Tuy nhiên, điều này cũng đang là vấn đề của công tác quản lý cả ở cấp vĩ mô và cấp cơ sở, khi hệ thống cơ sở pháp lý đang trong quá trình bổ sung, hoàn thiện. Mặt khác, về mặt quản lý, sự chưa đồng bộ và rạch ròi giữa các chức năng QLNN và quản trị nhà trường là những hạn chế, bước đầu được khắc phục. </div><div><span class="bold">Một số giải pháp đồng bộ</span></div><div>Từ những vấn đề nêu trên, để nâng cao chất lượng đào tạo nghề nghiệp, đáp ứng yêu cầu của nền kinh tế sáng tạo, trong lĩnh vực GDNN, trong thời gian tới, chúng ta cần thực hiện những giải pháp sau:</div><div><span class="bold"><span class="italic">1.</span></span><span class="bold"><span class="italic"> Về cơ chế chính sách:</span></span> Hoàn thiện các cơ chế chính sách, phù hợp với thực tiễn đối với đội ngũ nhà giáo, người học, cơ sở GDNN, người lao động trước khi tham gia TTLĐ, doanh nghiệp tham gia đào tạo, phân bổ và sử dụng tài chính trong lĩnh vực GDNN. Xây dựng các chuẩn chuyên môn, nghiệp vụ và kỹ năng sư phạm ở các cấp trình độ, kỹ năng ứng dụng CNTT trong thiết kế bài giảng. Đổi mới việc tuyển dụng, sử dụng, đào tạo, bồi dưỡng giáo viên cũng như chính sách về tiền lương nhằm thu hút người có kiến thức kỹ năng làm nhà giáo GDNN. Tăng cường tình tự chủ trong hoạt động đào tạo và quản trị nhà trường đối với các cơ sơ GDNN, nhằm tạo sự linh hoạt thích ứng với sự thay đổi của KH-CN và yêu cầu của TTLĐ. Các cơ sở GDNN tự chịu trách nhiệm về phát triển theo hướng tinh gọn, năng động, có khả năng làm việc trong môi trường cạnh tranh cao.</div><div><span class="bold"><span class="italic">2. Quản lý  và  ứng dụng CNTT:</span></span><span class="bold"> </span>hoàn thiện cơ chế,<br/> bộ máy quản lý nhà nước về GDNN theo hướng phân định rõ chức năng, nhiệm vụ, quyền hạn, gắn với trách nhiệm; giảm dần sự can thiệp của các cơ quan chủ quản vào các hoạt động đào tạo và quản trị nhà trường; chuẩn hóa, chuyên nghiệp hóa đội ngũ quản lý GDNN ở các cấp, nhất là ở cấp địa phương.</div><div>Ứng dụng mạnh mẽ CNTT trong công tác quản lý GDNN; đổi mới cơ chế tiếp nhận và xử lý thông tin; xây dựng cơ sở dữ liệu quốc gia về GDNN; xây dựng trung tâm tích hợp dữ liệu; trung tâm quản lý, điều hành tổng thể về GDNN; đầu tư các thiết bị, hệ thống thông tin quản lý; ứng dụng công nghệ thông tin vào các hoạt động quản lý dạy và học. Xây dựng thư viện điện tử, hệ thống đào tạo trực tuyến; khuyến khích các cơ sở  hình thành phòng học đa phương tiện, phòng chuyên môn hóa; hệ thống thiết bị ảo mô phỏng, thiết bị thực tế ảo, thiết bị dạy học thuật và các phần mềm ảo mô phỏng...</div><div><span class="bold"><span class="italic">3. Đổi mới hoạt động đào tạo:</span></span><span class="bold"> </span>Sẽ không còn khái niệm đào tạo theo niên chế, chương trình phải được thiết kế linh hoạt, đáp ứng chuẩn đầu ra của nghề và tạo sự liên thông giữa các trình độ trong một nghề và giữa các nghề. Đẩy mạnh các hoạt động nghiên cứu ứng dụng công nghệ, phương tiện dạy học cũng như công nghệ thông tin trong dạy học và quản lý đào tạo. Chú trọng các nghiên cứu mô phỏng, nghiên cứu tương tác người - máy. Hình thành mạng lưới nghiên cứu khoa học GDNN giữa các Viện, trường trong nước với các Viện, trường nước ngoài ở các nước tiên tiến như Cộng hòa Liên bang Đức, Hàn Quốc và các nước trong ASEAN và Châu Á khác...</div><div><span class="bold"><span class="italic">4.</span></span><span class="bold"><span class="italic"> Nâng cao năng lực, chất lượng giáo viên:</span></span><span class="bold"> </span>đội ngũ giáo viên phải có năng lực sáng tạo với những phẩm chất mới trên cơ sở chuẩn hóa, thông qua các hoạt động đào tạo, tự đào tạo và bồi dưỡng kiến thức chuyên môn, kỹ năng nghề, kỹ năng sư phạm và những kỹ năng mềm cần thiết khác. Chương trình, tài liệu đào tạo, bồi dưỡng nghiệp vụ sư phạm, kỹ năng nghề trên cơ sở chuẩn nhà giáo GDNN.</div><div>Đối với đội ngũ cán bộ quản lý phải có đủ năng lực làm việc trong môi trường sáng tạo cao và tự chịu trách nhiệm. Do vậy, cần tổ chức các hoạt động đào tạo, bồi dưỡng cả trong nước và ngoài nước để đáp ứng được yêu cầu công việc, có cơ chế sàng lọc để nâng cao chất lượng và hiệu quả công tác.</div><div><span class="bold"><span class="italic">5. Phát triển đào tạo tại doanh nghiệp:</span></span><span class="bold"> </span>trong môi trường 4.0, các hoạt động đào tạo cần phải được gắn kết với doanh nghiệp nhằm rút ngắn khoảng cách giữa đào tạo, nghiên cứu và triển khai. Đẩy mạnh phát triển đào tạo tại doanh nghiệp, phát triển các trường trong doanh nghiệp để đào tạo nhân lực phù hợp với công nghệ và tổ chức của doanh nghiệp. Tăng cường việc gắn kết giữa cơ sở GDNN và doanh nghiệp, trên cơ sở trách nhiệm xã hội của doanh nghiệp, hướng tới doanh nghiệp thực sự là “cánh tay nối dài” trong hoạt động đào tạo của cơ sở GDNN, nhằm sử dụng có hiệu quả trang thiết bị và công nghệ của doanh nghiệp phục vụ cho công tác đào tạo, hình thành năng lực nghề nghiệp cho người học trong quá trình đào tạo và thực tập tại doanh nghiệp.</div><div><span class="bold"> <span class="italic">6.Tăng cường hợp tác quốc tế:</span></span> các hoạt động hợp tác đa phương, song phương trong các lĩnh vực của GDNN như nghiên cứu khoa học, trao đổi học thuật; đào tạo, bồi dưỡng giáo viên, cán bộ quản lý; quản trị nhà trường cần được đẩy mạnh… Tạo điều kiện thuận lợi về môi trường pháp lý và xã hội để các nhà đầu tư nước ngoài mở cơ sở GDNN chất lượng cao tại Việt Nam; thực hiện liên kết, hợp tác tổ chức đào tạo nghề nghiệp. Đặc biệt, trong môi trường 4.0, phương pháp đào tạo cần phải thay đổi căn bản trên cơ sở lấy người học làm trung tâm và ứng dụng CNTT trong thiết kế bài giảng và truyền đạt bài giảng. Cùng với đó là sự đổi mới căn bản hình thức và phương pháp thi, kiểm tra trong GDNN theo hướng đáp ứng năng lực làm việc và tính sáng tạo của người học.</div><div><span class="bold">TS. Nguyễn Hồng Minh</span></div><div><span class="bold">Tổng Cục trưởng Tổng cục Dạy nghề</span><span class="bold">Khoa</span></div>
                    </div>
    '''
    s = get_soup(d)
    _combine_div_tags(s.div)
    print(s.div.prettify())
    return
    link = [
        'http://laodongxahoi.net/chuong-trinh-tuoi-gia-khong-co-don-trao-qua-tet-cho-cac-cu-cao-nien-o-huyen-soc-son-1305726.html',
        'http://laodongxahoi.net/bo-truong-dao-ngoc-dung-gap-mat-chuc-tet-can-bo-huu-tri-nhan-dip-xuan-dinh-dau-2017-1305713.html',
        'http://laodongxahoi.net/gap-mat-cac-can-bo-huu-tri-tai-phia-nam-1305712.html',
        'http://laodongxahoi.net/nga-chan-hon-900-phan-tu-khung-bo-am-muu-xam-nhap-lanh-tho-1305678.html'
    ]
    # result = crawler.crawl('http://www.phunutoday.vn/lam-me/')
    # result = normalizer.normalize('http://www.phunutoday.vn/clip-nhin-nhung-suat-com-nay-be-nha-ban-se-an-that-ngoan-d128693.html')
    # result = normalizer.normalize('http://www.phunutoday.vn/giam-5kg-sau-dung-1-tuan-khi-uong-nuoc-nay-truoc-bua-trua-15p-de-dien-do-di-choi-tet-am-lich-2017-d132354.html#1kBKJo5JqzR0yMca.97')
    # result = normalizer.normalize('http://www.phunutoday.vn/vbiz-25-1-ngoc-trinh-dap-tra-hoang-kieu-phi-thanh-van-len-tieng-chuyen-ly-hon-chong-tre-d134129.html#ix7o6Bq3KSyquzdr.97')
    # result = normalizer.normalize('http://www.phunutoday.vn/le-chua-dau-nam-2017-cung-sao-giai-han-the-nao-cho-dung-d133048.html#BLTvdE85svs3m65i.97')
    # result = normalizer.normalize('http://laodongxahoi.net/bo-truong-dao-ngoc-dung-gap-mat-chuc-tet-can-bo-huu-tri-nhan-dip-xuan-dinh-dau-2017-1305713.html')
    # result = normalizer.normalize('http://laodongxahoi.net/chi-bo-tap-chi-lao-dong-va-xa-hoi-hop-mat-ky-niem-87-nam-ngay-thanh-lap-dang-cong-san-viet-nam-1305763.html')
    # result = normalizer.normalize('http://www.nguoiduatin.vn/tin-moi-vu-o-to-16-cho-va-cham-tau-hoa-nhieu-nguoi-thuong-vong-a314398.html')
    result = normalizer.normalize(
        'http://laodongxahoi.net/cuoc-cach-mang-cong-nghiep-40-va-nhung-van-de-dat-ra-doi-voi-he-thong-giao-duc-nghe-nghiep-1305754.html')
    print(json.dumps(result, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
