# elasticsearch拼音多音词处理脚本
## 问题
使用<https://github.com/medcl/elasticsearch-analysis-pinyin>库，进行拼音分词。可能是多音词库不全，导致部分多音词搜索不到，比如： 了不起，使用liaobuqi无法搜索到，需要搜索lebuqi才能搜索到。

# 解决办法：
### 准备
* 从elasticsearch-analysis-pinyin项目中，找到依赖包： nlp-lang-1.7.jar
* 从nlp-lang-1.7.jar中解压出`pinyin.txt`及`polyphone.txt`文件。(可以直接使用winrar或其它压缩工具操作)
* 下载搜狗拼音词库
	* 项目地址：https://code.google.com/archive/p/hslinuxextra/downloads
	* 文件地址：https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/hslinuxextra/sougou-phrases-full.7z
* `sougou-phrases-full.7z`文件下载完成后，解压出其中的`fcitx/pyDhrase.org`文件，因为该文件是二进制的，容易分析。
* 将`pinyin.txt`及`polyphone.txt`,`pyDhrase.org`拷贝到与sougou_parse.py同一目录。

### 生成多音词词库映射
```
python sougou_parse.py > polyphone_mapping.txt
```
该脚本，会读取当前目录下的`pinyin.txt`及`pyDhrase.org`文件，通过分析，将`pyDhrase.org`中包含多音字的词语搜索出来，并按照nlp-lang中的格式，输出到`polyphone_mapping.txt`文件。(由于词语太多，该脚本只输出了长度小于等于4的词语)

### 使用词库
* 将`polyphone_mapping.txt`中的词典内容，拷贝并追加到`polyphone.txt`文件末尾。
* 将`polyphone.txt`文件重新添加到nlp-lang-1.7.jar文件中，并覆盖原来的词典文件。
* 将nlp-lang-1.7.jar覆盖项目中的nlp-lang-1.7.jar文件。
* 替换jar文件后，es中的索引数据要重建才能生效。

# 说明
* 简单查看了elasticsearch-analysis-pinyin的文档代码，没看到提供配置多音词字典的办法。所以才使用了上面不优雅的办法。
nlp-lang中是有暴露进口的，由于我对java也不太熟悉，所以没对elasticsearch-analysis-pinyin进行修改，所以直接将词典生成后，放到nlp-lang-1.7.jar中的默认资源文件中。
* 如果你嫌以上步骤操作过于麻烦，也可以直接使用本目录附带的nlp-lang-1.7.jar文件。
