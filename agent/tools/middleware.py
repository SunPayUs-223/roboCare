from typing import Callable

from langchain.agents import AgentState
from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from langchain_core.messages import ToolMessage
from langgraph.runtime import Runtime
from langgraph.types import Command

from utils.logger_handler import logger
from utils.prompt_loader import load_system_prompt, load_report_prompt


@wrap_tool_call
def monitor_tool(request: ToolCallRequest,
                 handler: Callable[[ToolCallRequest], ToolMessage | Command]) -> ToolMessage | Command:
    """
    监控工具调用
    :param request:
    :param handler:
    :return:
    """
    logger.info(f"[monitor_tool]执行工具：{request.tool_call['name']}")
    logger.info(f"[monitor_tool]传入参数：{request.tool_call['args']}")
    # 调用该工具时，改变标记’report‘的值
    if request.tool_call['name'] == "fill_context_for_report":
        request.runtime.context['report'] = True
    try:
        res = handler(request)
        logger.info(f"[monitor_tool]工具{request.tool_call['name']}调用成功！")
        return res
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败，原因：{str(e)}")
        raise e


@dynamic_prompt
def report_prompt_switch(request: ModelRequest):
    is_report = request.runtime.context.get('report', False)
    if is_report:
        return load_report_prompt()
    else:
        return load_system_prompt()


@before_model
def log_before_model(state: AgentState, runtime: Runtime):
    """
    :param state: 整个agent中的状态记录
    :param runtime:
    :return:
    """
    logger.info(f"即将调用模型,带有{len(state['messages'])}条消息")
