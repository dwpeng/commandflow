# commandflow

使用Python生成命令行

## 🍕 安装
```bash
pip install commandflow
```

## 🎉 快速开始

```py
from commandflow import Command
class MyCommand(Command):
    exe = 'fastp'

    def input(self, filename):
        self.set_action('f', 'file', value=filename)

if __name__ == '__main__':
    command = MyCommand()
    command.input('test.file')
    print(command.command)  # fastp --file test.file
```

## ✨文档

### 设计动机
1. 在进行生信分析时，往往会使用很多分析软件，当串联一个完整的分析流程时，需要编写大量的shell脚本，这很不优雅。
2. 我不喜欢写shell。


### 层次结构
![](./assert/layout.svg)
对于每一条命令Command而言，是由若干个Action组成，每一个Action为一个参数。

### 创建一个命令
```py
from commandflow import Command
class MyCommand(Command):
    exe = 'bwa'  # 指定可执行程序
```
或者也可以通过`set_exe()`来指定可执行程序
```py
from commandflow import Command
class MyCommand(Command):
    exe = 'bwa'  # 指定可执行程序

c = MyCommand()
c.set_exe('bwa')
```
### 添加参数
使用`set_action()`来添加参数到最终的命令行中
```py
from commandflow import Command
class MyCommand(Command):
    exe = 'bwa'

    def input(self, filename):
        self.set_action(
            'f',
            'file',
            value=filename
        )

c = MyCommand()
c.input('test.docx')
```
`set_action()`可以接收多个参数
```txt
- short_arg_name： 短参数名  -f
- long_arg_name： 长参数名  --file
- value：参数值
- help：对该条参数的解释说明
- positional：使用是一个位置参数，默认放到最后
- sep：当传递的value是一个list的时候，所指定的连接符，默认为空格
- stdout：命令是否需要指定标准输出
```
`value`可以为`int`、`float`、`str`、`list`类型的值，当`value`是一个`list`类型的值时，会通过`sep`连接起来，如当`sep`为空格时，`[1, 2, 3]`会被拼接为`1 2 3`，这对某些接收多个参数值的参数非常有用。


### 获取最终的命令行
```py
from commandflow import Command
class MyCommand(Command):
    exe = 'bwa'

    def input(self, filename):
        self.set_action(
            'f',
            'file',
            value=filename
        )

c = MyCommand()
c.input('test.docx')
print(c.command)  # bwa --file test.docx
```
当相同的参数值被多次设置参数时，后面设置的会将前面设置的覆盖
```py
c = MyCommand()
c.input('test.docx')
c.input('apple.docx')
print(c.command)  # bwa --file apple.docx
```


### 生成多个命令行
上面的方式只能生成一条命令，但实际应用中可能会涉及到需要生成多条命令，彼此之间只是参数值不同

使用`record()`记录需要生成的命令，并通过`records`来获取所有记录的命令
```py
c = MyCommand()
for file in ['1.docx', '2.docx', '3.docx']:
    c.input(file)
    c.record()

print(c.records)  # ['bwa --file 1.docx', 'bwa --file 2.docx', 'bwa --file 3.docx']
```

### 将所有命令重置（删除所有参数）
```py
c = MyCommand()
c.clear()
```


### 更改参数前面的前缀
有些软件中，可能参数名前面不是`-`、`--`，比如某些参数名并不是双短线跟着长参数名，而是短短线跟着长参数名，如`-file test.docx`。可以在继承的类中通过添加`long_dash`来声明长参数名的前缀，`short_dash`来声明短参数名的前缀。

```py
from commandflow import Command
class MyCommand(Command):
    long_dash = '-'
    short_dash = '-'
    exe = 'bwa'
```

### 后台任务
```py
c.nohup(nohup=True, nohup_log=False)
c.input('apple.docx')
print(c.command)
# nohup bwa --file apple.docx >/dev/null 2>&1
```
