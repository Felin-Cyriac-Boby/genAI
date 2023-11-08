

from haystack.nodes import PromptNode

from haystack.pipelines import Pipeline

from haystack.agents.memory import ConversationSummaryMemory
from haystack.agents.conversational import ConversationalAgent



def init_promptnode():
    prompt_node = PromptNode()
    return prompt_node

prompt_node = init_promptnode()
summary_memory = ConversationSummaryMemory(prompt_node)

def init_agent():
    conversational_agent = ConversationalAgent(prompt_node = prompt_node, memory = summary_memory)
    return conversational_agent