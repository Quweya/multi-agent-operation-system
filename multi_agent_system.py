import asyncio
import sqlite3
import logging
from datetime import datetime

# =========================
# 日志系统
# =========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# =========================
# 数据库初始化
# =========================
conn = sqlite3.connect("agent_system.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent TEXT,
    task TEXT,
    result TEXT,
    created_at TEXT
)
''')

conn.commit()

# =========================
# Agent基类
# =========================
class BaseAgent:

    def __init__(self, name):
        self.name = name

    async def process(self, task):
        raise NotImplementedError

    def save_result(self, task, result):
        cursor.execute(
            "INSERT INTO tasks (agent, task, result, created_at) VALUES (?, ?, ?, ?)",
            (
                self.name,
                task,
                result,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        conn.commit()

# =========================
# 市场调研Agent
# =========================
class ResearchAgent(BaseAgent):

    async def process(self, task):
        logging.info(f"{self.name} 正在分析市场趋势...")

        await asyncio.sleep(2)

        result = (
            "热门AI内容方向：\n"
            "1. AI绘画\n"
            "2. AI短视频\n"
            "3. AI数字人\n"
            "4. AI自动化运营"
        )

        self.save_result(task, result)

        return result

# =========================
# 内容生成Agent
# =========================
class ContentAgent(BaseAgent):

    async def process(self, task):
        logging.info(f"{self.name} 正在生成内容...")

        await asyncio.sleep(2)

        result = (
            "短视频文案：\n"
            "《AI已经开始替代运营团队了吗？》\n"
            "今天带你看看AI多Agent系统如何自动完成运营工作！"
        )

        self.save_result(task, result)

        return result

# =========================
# 数据分析Agent
# =========================
class AnalyticsAgent(BaseAgent):

    async def process(self, task):
        logging.info(f"{self.name} 正在分析数据...")

        await asyncio.sleep(2)

        result = (
            "数据分析结果：\n"
            "AI运营类内容近30天增长率提升35%\n"
            "用户最关注：自动赚钱、AI创业、自动化"
        )

        self.save_result(task, result)

        return result

# =========================
# Manager Agent
# =========================
class ManagerAgent(BaseAgent):

    def __init__(self, name, agents):
        super().__init__(name)
        self.agents = agents

    async def process(self, task):

        logging.info("Manager开始拆解任务")

        # 并发执行多个Agent
        results = await asyncio.gather(
            self.agents[0].process(task),
            self.agents[1].process(task),
            self.agents[2].process(task)
        )

        final_result = "\n\n".join(results)

        self.save_result(task, final_result)

        return final_result

# =========================
# 任务调度器
# =========================
class TaskScheduler:

    def __init__(self):
        self.queue = asyncio.Queue()

    async def add_task(self, task):
        await self.queue.put(task)

    async def run(self, manager_agent):

        while not self.queue.empty():
            task = await self.queue.get()

            logging.info(f"开始执行任务: {task}")

            result = await manager_agent.process(task)

            print("\n========== 最终结果 ==========")
            print(result)
            print("=============================\n")

            self.queue.task_done()

# =========================
# 主程序
# =========================
async def main():

    # 初始化Agent
    research_agent = ResearchAgent("ResearchAgent")
    content_agent = ContentAgent("ContentAgent")
    analytics_agent = AnalyticsAgent("AnalyticsAgent")

    manager_agent = ManagerAgent(
        "ManagerAgent",
        [
            research_agent,
            content_agent,
            analytics_agent
        ]
    )

    # 初始化调度器
    scheduler = TaskScheduler()

    # 添加任务
    await scheduler.add_task(
        "生成AI自媒体运营方案"
    )

    await scheduler.add_task(
        "分析AI短视频趋势"
    )

    # 启动调度
    await scheduler.run(manager_agent)

# =========================
# 程序入口
# =========================
if __name__ == "__main__":
    asyncio.run(main())
