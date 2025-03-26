# srt-GPT-translator
这个工具旨在帮助用户使用 LLM API 将 字幕文件（.srt, .vtt）翻译成另一种语言。支持双语字幕输出。

## 特点
- 每次翻译为不超过1024字符的多个字幕块，以保持上下文的通畅
- 加入了检测翻译结果的机制，若格式与原文不对应，会重新翻译，翻译三次仍然不对，会返回那一部分短文本原文


## 安装

要使用此工具，您需要在系统上安装Python 3，以及以下软件包：

您可以通过运行以下命令来安装这些软件包：

`pip install -r requirements.txt` 


## 用法

使用此工具，您需要首先将 settings.cfg.example 重命名为 settings.cfg。

```
cd srt-gpt-translator
mv settings.cfg.example settings.cfg
nano settings.cfg` 
```

`apikey = sk-xxxxxxx` 

将sk-xxxxxxx替换为您的 LLM API密钥。 更改其他选项，然后保存。

运行命令：
```
python3 srt_translation.py [-h] [--test] filename

positional arguments:
  filename    输入文件的名称

options:
  -h，--help  显示此帮助消息并退出
  --test      只翻译前3个短文本
```

只需使用要翻译或转换的文件作为参数运行`srt_translation.py`脚本即可。例如，要翻译名为`example.srt`的SRT文件，您将运行以下命令：

`python3 srt_translation.py example.srt` 

默认情况下，脚本将尝试将文本翻译成`settings.cfg`文件中`target-language`选项下指定的语言。

## 特征

-   该代码从settings.cfg文件中读取 LLM API 密钥，目标语言和其他选项。
-   代码提供了进度条，以显示SRT翻译的进度。
-   测试功能可用。只翻译3个短文本以节省API使用情况，使用--test选项。

## 配置

`settings.cfg`文件包含几个选项，可用于配置脚本的行为：

-   `base-url`：API Base URL
-   `api-key`： API 密钥
-   `target-language`：文本翻译成的语言，会应用在提示语中（例如：Simplified Chinese）。
-   `target-lang`：语言区域代码，会应用在翻译后的文件名中（例如：zh-CN）。

## 输出

脚本的输出的文件：
- 一个与输入文件同名的字幕文件，在文件名中添加了语言区域代码。例如：输入文件是`example.srt`，则输出文件将为`example.zh-CN.srt`。
