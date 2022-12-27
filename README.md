# bioflow

## 背景
在分析数据的时候，经常需要编写shell脚本，虽然很多时候写起来并不麻烦，但是总有遇到忘记某个参数是什么意思的时候。所以就有了通过Python去生成一串命令的想法。

## 使用指南

## Python版本要求
本程序使用了类型注释，请确保python版本大于`3.7+`，推荐使用`3.9+`

### 开发
本程序使用`poetry作为包管理器`，所以请确保你的电脑上安装有`poetry`
```bash
pip install poetry
```
### 安装

#### 使用pip安装
```py
pip install bioflow
```

#### 使用poetry打包安装

先使用`poetry build`进行打包，然后使用`pip install ./dist/*.whl`进行安装

```bash
poetry build
pip install .\dist\bioflow-0.1.0-py3-none-any.whl --force-reinstall
```


### 首先继承继承Command类
```py
from bioflow import Command
class Fastp(Command):
    # 设置可执行程序的名字
    # 这里也可以直接写成一个可执行程序的路径
    exe = 'fastp'
    ...
```

`Command`使用`set_action`方法设置参数，这里的方法设计灵感来自于`argparse`这个标准库

方法原型

```py
def set_action(
    self,
    short_arg_name: Union[str, None] = None,
    long_arg_name: Union[str, None] = None,
    value: Union[str, bool, List, None] = None,
    help: Union[str, None] = None,
    positional: bool = False,
    sep: str = ' ',
    stdout: Union[str, None] = None
):
    ...
```
- short_arg_name： 短参数名
- long_arg_name： 长参数名
- value：参数值
- help：对该条参数的解释说明
- positional：使用是一个位置参数
- sep：当传递的value是一个list的时候，所指定的连接符，默认为空格
- stdout：命令是否需要指定标准输出

`value`可以接收以下几种的类型的参数值
- list
- int
- float
- str
- bool


可以添加自定义方法来组合参数

```py
from bioflow import Command
class Fastp(Command):
    # 设置可执行程序的名字
    # 这里也可以直接写成一个可执行程序的路径
    exe = 'fastp'

    # 设置了一个组合方法
    # 内部使用set_action来设置具体的参数
    def input(
        self,
        in1: str,
        out1: str,
        in2: str = None,
        out2: str = None,
        phred64: bool = True,
        compression_level: int = 4,
    ):
        """ 输入输出 """
        self.set_action('i', 'in1', in1)
        self.set_action('o', 'out1', out1)

        if in2 is not None and out2 is not None:
            self.set_action('I', 'in2', in2)
            self.set_action('O', 'out2', out2)

        self.set_action('6', 'phred64', phred64)
        self.set_action('z', 'compression', compression_level)
```

对于一个相同的参数而言，重复设置时，以后来的为准
```py
self.set_action('i', 'in1', 'before')
self.set_action('i', 'in1', 'after')  # in1 参数值为after，之前的before被后来的替换掉了
```

使用`.command`来获取拼接好的完整命令
```py
fastp = Fastp()
fastp.input('1.fq', '1.out.fq', '2.fq', '2.out.fq')
print(fastp.command)
# fastp --in1 1.fq --out1 1.out.fq --in2 2.fq --out2 2.out.fq --phred64 --compression 4
```

## 具体的例子

这里使用bioflow编写fastp程序对应的参数（写了一部分）
```txt

r"""
usage: fastp -i <in1> -o <out1> [-I <in1> -O <out2>] [options...]
options:
  # I/O options
  -i, --in1                          read1 input file name (string)
  -o, --out1                         read1 output file name (string [=])
  -I, --in2                          read2 input file name (string [=])
  -O, --out2                           read2 output file name (string [=])
      --unpaired1                      for PE input, if read1 passed QC but read2 not, it will be written to unpaired1. Default is to discard it. (string [=])
      --unpaired2                      for PE input, if read2 passed QC but read1 not, it will be written to unpaired2. If --unpaired2 is same as --unpaired1 (default mode), both unpaired reads will be written to this same file. (string [=])
      --failed_out                     specify the file to store reads that cannot pass the filters. (string [=])
      --overlapped_out                 for each read pair, output the overlapped region if it has no any mismatched base. (string [=])
  -m, --merge                          for paired-end input, merge each pair of reads into a single read if they are overlapped. The merged reads will be written to the file given by --merged_out, the unmerged reads will be written to the files specified by --out1 and --out2. The merging mode is disabled by default.
      --merged_out                     in the merging mode, specify the file name to store merged output, or specify --stdout to stream the merged output (string [=])
      --include_unmerged               in the merging mode, write the unmerged or unpaired reads to the file specified by --merge. Disabled by default.
  -6, --phred64                      indicate the input is using phred64 scoring (it'll be converted to phred33, so the output will still be phred33)
  -z, --compression                  compression level for gzip output (1 ~ 9). 1 is fastest, 9 is smallest, default is 4. (int [=4])
      --stdin                          input from STDIN. If the STDIN is interleaved paired-end FASTQ, please also add --interleaved_in.
      --stdout                         output passing-filters reads to STDOUT. This option will result in interleaved FASTQ output for paired-end input. Disabled by default.
      --interleaved_in                 indicate that <in1> is an interleaved FASTQ which contains both read1 and read2. Disabled by default.
      --reads_to_process             specify how many reads/pairs to be processed. Default 0 means process all reads. (int [=0])
      --dont_overwrite               don't overwrite existing files. Overwritting is allowed by default.
      --fix_mgi_id                     the MGI FASTQ ID format is not compatible with many BAM operation tools, enable this option to fix it.

  # adapter trimming options
  -A, --disable_adapter_trimming     adapter trimming is enabled by default. If this option is specified, adapter trimming is disabled
  -a, --adapter_sequence               the adapter for read1. For SE data, if not specified, the adapter will be auto-detected. For PE data, this is used if R1/R2 are found not overlapped. (string [=auto])
      --adapter_sequence_r2            the adapter for read2 (PE data only). This is used if R1/R2 are found not overlapped. If not specified, it will be the same as <adapter_sequence> (string [=])
      --adapter_fasta                  specify a FASTA file to trim both read1 and read2 (if PE) by all the sequences in this FASTA file (string [=])
      --detect_adapter_for_pe          by default, the adapter sequence auto-detection is enabled for SE data only, turn on this option to enable it for PE data.
    
  # global trimming options
  -f, --trim_front1                    trimming how many bases in front for read1, default is 0 (int [=0])
  -t, --trim_tail1                     trimming how many bases in tail for read1, default is 0 (int [=0])
  -b, --max_len1                       if read1 is longer than max_len1, then trim read1 at its tail to make it as long as max_len1. Default 0 means no limitation (int [=0])
  -F, --trim_front2                    trimming how many bases in front for read2. If it's not specified, it will follow read1's settings (int [=0])
  -T, --trim_tail2                     trimming how many bases in tail for read2. If it's not specified, it will follow read1's settings (int [=0])
  -B, --max_len2                       if read2 is longer than max_len2, then trim read2 at its tail to make it as long as max_len2. Default 0 means no limitation. If it's not specified, it will follow read1's settings (int [=0])

  # duplication evaluation and deduplication
  -D, --dedup                          enable deduplication to drop the duplicated reads/pairs
      --dup_calc_accuracy              accuracy level to calculate duplication (1~6), higher level uses more memory (1G, 2G, 4G, 8G, 16G, 24G). Default 1 for no-dedup mode, and 3 for dedup mode. (int [=0])
      --dont_eval_duplication          don't evaluate duplication rate to save time and use less memory.

  # polyG tail trimming, useful for NextSeq/NovaSeq data
  -g, --trim_poly_g                  force polyG tail trimming, by default trimming is automatically enabled for Illumina NextSeq/NovaSeq data
      --poly_g_min_len                 the minimum length to detect polyG in the read tail. 10 by default. (int [=10])
  -G, --disable_trim_poly_g          disable polyG tail trimming, by default trimming is automatically enabled for Illumina NextSeq/NovaSeq data

  # polyX tail trimming
  -x, --trim_poly_x                    enable polyX trimming in 3' ends.
      --poly_x_min_len                 the minimum length to detect polyX in the read tail. 10 by default. (int [=10])
  
  # per read cutting by quality options
  -5, --cut_front                      move a sliding window from front (5') to tail, drop the bases in the window if its mean quality < threshold, stop otherwise.
  -3, --cut_tail                       move a sliding window from tail (3') to front, drop the bases in the window if its mean quality < threshold, stop otherwise.
  -r, --cut_right                      move a sliding window from front to tail, if meet one window with mean quality < threshold, drop the bases in the window and the right part, and then stop.
  -W, --cut_window_size                the window size option shared by cut_front, cut_tail or cut_sliding. Range: 1~1000, default: 4 (int [=4])
  -M, --cut_mean_quality               the mean quality requirement option shared by cut_front, cut_tail or cut_sliding. Range: 1~36 default: 20 (Q20) (int [=20])
      --cut_front_window_size          the window size option of cut_front, default to cut_window_size if not specified (int [=4])
      --cut_front_mean_quality         the mean quality requirement option for cut_front, default to cut_mean_quality if not specified (int [=20])
      --cut_tail_window_size           the window size option of cut_tail, default to cut_window_size if not specified (int [=4])
      --cut_tail_mean_quality          the mean quality requirement option for cut_tail, default to cut_mean_quality if not specified (int [=20])
      --cut_right_window_size          the window size option of cut_right, default to cut_window_size if not specified (int [=4])
      --cut_right_mean_quality         the mean quality requirement option for cut_right, default to cut_mean_quality if not specified (int [=20])
  
  # quality filtering options
  -Q, --disable_quality_filtering    quality filtering is enabled by default. If this option is specified, quality filtering is disabled
  -q, --qualified_quality_phred      the quality value that a base is qualified. Default 15 means phred quality >=Q15 is qualified. (int [=15])
  -u, --unqualified_percent_limit    how many percents of bases are allowed to be unqualified (0~100). Default 40 means 40% (int [=40])
  -n, --n_base_limit                 if one read's number of N base is >n_base_limit, then this read/pair is discarded. Default is 5 (int [=5])
  -e, --average_qual                 if one read's average quality score <avg_qual, then this read/pair is discarded. Default 0 means no requirement (int [=0])

  # length filtering options
  -L, --disable_length_filtering     length filtering is enabled by default. If this option is specified, length filtering is disabled
  -l, --length_required              reads shorter than length_required will be discarded, default is 15. (int [=15])
      --length_limit                 reads longer than length_limit will be discarded, default 0 means no limitation. (int [=0])

  # low complexity filtering
  -y, --low_complexity_filter          enable low complexity filter. The complexity is defined as the percentage of base that is different from its next base (base[i] != base[i+1]).
  -Y, --complexity_threshold           the threshold for low complexity filter (0~100). Default is 30, which means 30% complexity is required. (int [=30])

  # filter reads with unwanted indexes (to remove possible contamination)
      --filter_by_index1               specify a file contains a list of barcodes of index1 to be filtered out, one barcode per line (string [=])
      --filter_by_index2               specify a file contains a list of barcodes of index2 to be filtered out, one barcode per line (string [=])
      --filter_by_index_threshold      the allowed difference of index barcode for index filtering, default 0 means completely identical. (int [=0])

  # base correction by overlap analysis options
  -c, --correction                   enable base correction in overlapped regions (only for PE data), default is disabled
      --overlap_len_require            the minimum length to detect overlapped region of PE reads. This will affect overlap analysis based PE merge, adapter trimming and correction. 30 by default. (int [=30])
      --overlap_diff_limit             the maximum number of mismatched bases to detect overlapped region of PE reads. This will affect overlap analysis based PE merge, adapter trimming and correction. 5 by default. (int [=5])
      --overlap_diff_percent_limit     the maximum percentage of mismatched bases to detect overlapped region of PE reads. This will affect overlap analysis based PE merge, adapter trimming and correction. Default 20 means 20%. (int [=20])

  # UMI processing
  -U, --umi                          enable unique molecular identifier (UMI) preprocessing
      --umi_loc                      specify the location of UMI, can be (index1/index2/read1/read2/per_index/per_read, default is none (string [=])
      --umi_len                      if the UMI is in read1/read2, its length should be provided (int [=0])
      --umi_prefix                   if specified, an underline will be used to connect prefix and UMI (i.e. prefix=UMI, UMI=AATTCG, final=UMI_AATTCG). No prefix by default (string [=])
      --umi_skip                       if the UMI is in read1/read2, fastp can skip several bases following UMI, default is 0 (int [=0])

  # overrepresented sequence analysis
  -p, --overrepresentation_analysis    enable overrepresented sequence analysis.
  -P, --overrepresentation_sampling    One in (--overrepresentation_sampling) reads will be computed for overrepresentation analysis (1~10000), smaller is slower, default is 20. (int [=20])

  # reporting options
  -j, --json                         the json format report file name (string [=fastp.json])
  -h, --html                         the html format report file name (string [=fastp.html])
  -R, --report_title                 should be quoted with ' or ", default is "fastp report" (string [=fastp report])
  
  # threading options
  -w, --thread                       worker thread number, default is 3 (int [=3])
  
  # output splitting options
  -s, --split                        split output by limiting total split file number with this option (2~999), a sequential number prefix will be added to output name ( 0001.out.fq, 0002.out.fq...), disabled by default (int [=0])
  -S, --split_by_lines               split output by limiting lines of each file with this option(>=1000), a sequential number prefix will be added to output name ( 0001.out.fq, 0002.out.fq...), disabled by default (long [=0])
  -d, --split_prefix_digits          the digits for the sequential number padding (1~10), default is 4, so the filename will be padded as 0001.xxx, 0 to disable padding (int [=4])
  
  # help
  -?, --help                         print this message
"""

```

## 代码

```py
from typing import Literal
from bioflow import Command

class Fastp(Command):
    exe = 'fastp'

    def input(
        self,
        in1: str,
        out1: str,
        in2: str = None,
        out2: str = None,
        phred64: bool = True,
        compression_level: int = 4,
    ):
        """ 输入输出 """
        self.set_action('i', 'in1', in1)
        self.set_action('o', 'out1', out1)

        if in2 is not None and out2 is not None:
            self.set_action('I', 'in2', in2)
            self.set_action('O', 'out2', out2)

        self.set_action('6', 'phred64', phred64)
        self.set_action('z', 'compression', compression_level)


    def adapter_trim(
        self,
        enable: bool = True,
        adapter_sequence: str = 'auto'
    ):
        """ 接头修剪 """
        self.set_action('A', 'disable_adapter_trimming', enable)
        self.set_action('a', 'adapter_sequence', adapter_sequence)

    def global_trim(
        self,
        trim_front1: int = 0,
        trim_tail1: int = 0,
        max_len1: int = 0,
        trim_front2: int = 0,
        trim_tail2: int = 0,
        max_len2: int = 0,
    ):
        """ 切割参数 """
        self.set_action('f', 'trim_front1', trim_front1)
        self.set_action('t', 'trim_tail1', trim_tail1)
        self.set_action('b', 'max_len1', max_len1)
        
        self.set_action('F', 'trim_front2', trim_front2)
        self.set_action('T', 'trim_tail2', trim_tail2)
        self.set_action('B', 'max_len2', max_len2)
    
    def thread(self, count: int = 3):
        """ 线程数 """
        assert count > 0
        self.set_action('w', 'thread', count)

    def trim_polyg(
        self,
        enable: bool = True,
        polyg_min_len: int = 10,
    ):
        """ poly G尾巴处理 """
        if enable:
            self.set_action('g', 'trim_poly_g', True)
            self.set_action(None, 'poly_g_min_len', polyg_min_len)
        else:
            self.set_action('G', 'disable_trim_poly_g', True)

    def quality(
        self,
        enable: bool = True,
        qualified_quality_phred: int = 15,
        unqualified_percent_limit: int = 40,
        n_base_limit: int = 5,
        average_qual: int = 0
    ):
        """ 质量控制 """
        if not enable:
            self.set_action('Q', 'disable_quality_filtering', True)
            return self

        self.set_action('q', 'qualified_quality_phred', qualified_quality_phred)
        self.set_action('u', 'unqualified_percent_limit', unqualified_percent_limit),
        self.set_action('n', 'n_base_limit', n_base_limit),
        self.set_action('e', 'average_qual', average_qual)

    def report(
        self,
        json: str = 'report.json',
        html: str = 'report.html'
    ):
        """ 输出的报告形式 """
        self.set_action(None, 'html', html)
        self.set_action(None, 'json', json)

    def umi_processing(
        self,
        enable: bool = True,
        umi_loc: Literal['index1', 'index2', 'read1',
                         'read2', 'per_index', 'per_read' 'none'] = 'none',
        umi_len: int = 0,
        umi_prefix: str = 'UMI',
        umi_skip: int = 0
    ):
        """ 处理umi """
        self.set_action('U', 'umi', enable)
        if umi_loc != 'none':
            self.set_action(None, 'umi_loc', umi_loc)
        if umi_loc in ['read1', 'read2']:
            self.set_action(None, 'umi_len', umi_len)
            self.set_action(None, 'umi_prefix', umi_prefix)
            self.set_action(None, 'umi_skip', umi_skip)



if __name__ == '__main__':
    fastp = Fastp()
    fastp.input('1.fq', '1.out.fq', '2.fq', '2.out.fq')
    print(fastp.command)
    fastp.input('3.fa', '111', 'sss', 'hhhh')
    fastp.report()
    fastp.stdout()
    fastp.thread(100)
    print(fastp.command)

```
