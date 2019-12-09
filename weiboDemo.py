import uiautomator2 as u2
import hashlib
import pandas as pd
"""
使用uiautomator2 对新浪微博app的原创内容 转发 评论 点赞 等信息进行抓取
weibo_counts 设置需要抓取的微博数
"""
# need to crawler weibo
weibo_counts = 185
# 在pandas写excel时候先确定一个全局的datas内容格式
rows = {"文章": [], "转发": [], "评论": [], "点赞":[]}

# 定义一个方法用来给文字用md5加密
def hash_encode(encodestr):
    # hash 算法加密
    m = hashlib.md5()
    # utf-8 编码
    b = encodestr.encode(encoding='utf-8')
    m.update(b)
    # 加密
    str_md5 = m.hexdigest()
    return str_md5

# 具体执行的方法
def executes():
    # 输入设备码 由 adb devices 指令获得
    d = u2.connect_usb("PNXGAM48A2401257")
    original_article = ""
    original_other = ""
    # 计数  如果微博达到weibo_counts 说明抓完了 从0开始计算
    flag = 0
    # 重复内容计数
    repeat_content = 0
    # 开始循环
    while True:
        content = d(className="android.widget.LinearLayout")
        try:
            # 得到抓的LinearLayout 中的文章信息，转发，评论和点赞
            article = str(
                content.child_selector(resourceId="com.sina.weibo:id/contentTextView").info["contentDescription"])
            report = str(content.child_selector(resourceId="com.sina.weibo:id/leftButton").info["contentDescription"])
            comment = str(content.child_selector(resourceId="com.sina.weibo:id/midButton").info["contentDescription"])
            zan = str(content.child_selector(resourceId="com.sina.weibo:id/rightButton").child_selector(
                className="android.widget.TextView").info["text"])
        except Exception as e:
            print("内容异常，继续向下滑动")
            d.swipe(0, 0.936, 0, 0.822, )
            continue
        if flag == weibo_counts:
            print("完成了")
            break
        # 如果不是第一条数据 且 （哈希后的文章或哈希后的转发+评论的值只要有一个相同那么就说明抓的LinearLayout的包含的内容有偏差--文章可能和转发评论不是一个微博框中的值需要滑动手机继续抓取）
        elif flag != 0 and (
                hash_encode(original_article) == hash_encode(article) or hash_encode(original_other) == hash_encode(
                report + comment)):
            # 按纵坐标滑动
            d.swipe(0, 0.936, 0, 0.822, )
            # 如果重复出现一个内容到达10次以上说明已经滑动到头了
            if repeat_content >= 10:
                break
            # 重复内容+1
            repeat_content += 1

        else:
            # 将原始的文章内容和原始的转发评论更新。方便以后新的内容获取之后进行对比
            original_article = article
            original_other = report + comment
            zan = "点赞" + zan
            # 标记抓了多少个微博 flag+1
            flag += 1
            #  然后输入文章内容和转发评论数
            rows["文章"].append(article.strip())
            rows["转发"].append(report.strip())
            rows["评论"].append(comment.strip())
            rows["点赞"].append(zan.strip())

    # 将rows字典包含的内容 通过DataFrame 写入到我们自定义的文件中
    datas = pd.DataFrame(rows)
    datas.to_excel("ifind.xlsx")


if __name__ == '__main__':
    executes()






























































































































































































