from langchain.agents import create_agent

from agent.tools.agent_tools import rag_summarize, get_weather, get_user_id, get_user_location, get_current_month, \
    fill_context_for_report, fetch_external_data
from agent.tools.middleware import monitor_tool, report_prompt_switch, log_before_model
from model.model_factory import chat_model
from utils.prompt_loader import load_system_prompt


class ReactAgent:
    def __init__(self):
        self.agent = create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize, get_weather, get_user_id, get_user_location, get_current_month,
                   fetch_external_data, fill_context_for_report],
            middleware=[monitor_tool, report_prompt_switch, log_before_model],
        )

    def execute_stream(self, query):
        input_dic = {
            "messages": [{"role": "user", "content": query}]
        }
        # report先初始化，否则后续修改会报错
        res = self.agent.stream(input=input_dic, stream_mode="values", context={"report": False})
        for chunk in res:
            msg = chunk["messages"][-1]  # 最后一条
            if msg.content:
                yield msg.content.strip() + "\n"


if __name__ == '__main__':
    agent = ReactAgent()
    # for chunk in agent.execute_stream("扫地机器人在我所在的地区的气温下如何保养？"):
    for chunk in agent.execute_stream("给我生成我的使用报告"):
        print(chunk, end="", flush=True)
