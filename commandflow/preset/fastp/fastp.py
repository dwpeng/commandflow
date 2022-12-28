from typing import Literal
from commandflow import Command

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
    for i in range(10):
        fastp.input(f'{i}.fq', f'{i + 1}.fq',f'{i}.fq', f'{i + 1}.fq' )
        for j in range(3):
            fastp.stdout(f'{j}')
            fastp.set_subcommand('merge')
            fastp.record()
    print('\n'.join(fastp.records))
