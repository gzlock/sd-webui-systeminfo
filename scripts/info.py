import gradio as gr
from fastapi import FastAPI
import sys
import jinja2


table_template = """
<table>
    <thead>
        <tr>
            <th>{header1}</th>
            <th>{header2}</th>
        </tr>
    </thead>
    <tbody>
        {rows}
    </tbody>
</table>
"""

rows_template = """
<tr>
    <td>{cell1}</td>
    <td>{cell2}</td>
</tr>
"""


def on_ui_tabs():
    with gr.Blocks(analytics_enabled=False) as system_info:
        if sys.platform == "win32":
            import wmi
            w = wmi.WMI()
            with gr.Column():
                rows = ""
                # 获取CPU信息
                for index, processor in enumerate(w.Win32_Processor()):
                    rows += rows_template.format(
                        cell1=f'CPU {index}', cell2=processor.Name.strip())
                
                # 获取显卡信息
                for index, gpu in enumerate(w.Win32_VideoController()):
                    rows += rows_template.format(
                        cell1=f'GPU {index}', cell2=gpu.Name.strip())

                # 获取内存信息
                for index, memory in enumerate(w.Win32_PhysicalMemory()):
                    rows += rows_template.format(
                        cell1=f'Memory {index}', cell2=f'{int(memory.Capacity) / (1024 ** 3)} GB')

                gr.HTML(table_template.format(
                    header1='Hardware', header2='Model', rows=rows))
        else:
            gr.HTML('Sorry, only support Windows platform.')

    return [(system_info, "System Info", "system_info")]


try:
    import modules.script_callbacks as script_callbacks

    script_callbacks.on_ui_tabs(on_ui_tabs)
except:
    pass
