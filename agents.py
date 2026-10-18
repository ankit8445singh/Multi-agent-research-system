from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# ==========================================
# MODEL SETUP: GROQ
# ==========================================

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0
)


# ==========================================
# 1. SEARCH AGENT
# ==========================================

def build_search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are an expert research search agent. "
            "Use the web_search tool to find relevant, reliable "
            "and recent information about the user's topic. "
            "Include source URLs and useful findings in your response. "
            "Do not invent sources or facts."
        )
    )


# ==========================================
# 2. READER AGENT
# ==========================================

def build_reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url],
        system_prompt=(
            "You are an expert web research reader. "
            "Use the scrape_url tool to extract useful information "
            "from the supplied URLs. Summarize the main findings, "
            "important facts and evidence. Preserve source URLs. "
            "Do not invent information."
        )
    )


# ==========================================
# 3. WRITER CHAIN
# ==========================================

writer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert research writer.

        Write clear, structured, factual and insightful research reports.
        Use only the supplied research and distinguish established facts
        from uncertain claims.
        Do not invent facts, statistics, quotations or sources.
        """
    ),
    (
        "human",
        """
        Write a detailed research report on the topic below.

        Topic:
        {topic}

        Research Gathered:
        {research}

        Follow this structure:

        1. Introduction
        2. Key Findings
           - Include at least 3 well-explained findings.
           - Explain their significance.
        3. Conclusion
        4. Sources
           - List the source URLs present in the research.
           - Do not invent URLs.

        Write professionally and avoid unnecessary repetition.
        """
    ),
])

writer_chain = writer_prompt | llm | StrOutputParser()


# ==========================================
# 4. CRITIC CHAIN
# ==========================================

critic_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a strict and constructive research report evaluator.

        Evaluate factual accuracy, depth, organization, clarity,
        evidence quality and source reliability.

        Be honest, specific and constructive.
        Do not assume that unsupported claims are true.
        """
    ),
    (
        "human",
        """
        Review the research report below and evaluate it strictly.

        Report:
        {report}

        Respond in this exact format:

        Score: X/10

        Strengths:
        - ...
        - ...

        Areas to Improve:
        - ...
        - ...

        One line verdict:
        ...
        """
    ),
])

critic_chain = critic_prompt | llm | StrOutputParser()

