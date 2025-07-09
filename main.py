from crewai import Agent, Task, Crew, Process
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import os
from youtube_transcriptions import get_latest_youtube_transcription 
from dotenv import load_dotenv

load_dotenv()

def main(user_input: str):
    # Create a StdioServerParameters object
    server_params=StdioServerParameters(
        command="python3", 
        args=["mcp_servers/instagram_server.py"],
        env={
            "INSTAGRAM_ACCESS_TOKEN": os.getenv("INSTAGRAM_ACCESS_TOKEN"),
            "INSTAGRAM_ACCOUNT_ID": os.getenv("INSTAGRAM_ACCOUNT_ID"),
            "HOST_URL": os.getenv("HOST_URL"),
            "LATEST_API_VERSION": os.getenv("LATEST_API_VERSION")
        },
    )

    with MCPServerAdapter(server_params) as tools:
        print(f"Available tools from Stdio MCP server: {[tool.name for tool in tools]}")
        
        instagram_agent = Agent(
            role="Instagram Agent",
            goal="Post to Instagram",
            backstory="An AI that leverages local scripts via Model Context Protocol for posting to Instagram.  You are an expert in python and instagram.",
            tools=tools,
            reasoning=True,
            verbose=True,
        )
        
        processing_task = Task(
            description=f"""
                Post a post to Instagram.  The post should be a single image with a caption. 
                
                For the caption, turn this into a carousel post with 7 steps:
                {get_latest_youtube_transcription()}
                
                Format the caption:
                1. Markdown-like formatting (examples):
                    - Bold: While there isn't official Markdown support for posts, you can try using double asterisks ** around the text you want to bold. For example, **This text will be bold.**.
                    - Italic: Similarly, single asterisks * around text might result in italics. For example, *This text might be italic.*. 
                    
                2. Use \r\n to insert line breaks in your text. For example: content: Hello \r\n World. 
                This shouldn't be too long, but explained in steps.  Again, this is for an instagram post where I will be backing with images.
                
                Then post that along with the image to instagram.
                The image urls are:
                https://social-images-tylerai.s3.us-east-2.amazonaws.com/bolt-new/Build+a+Habit+Tracker+Inspired+by+Atomic+Habits+-+slide1.png
                https://social-images-tylerai.s3.us-east-2.amazonaws.com/bolt-new/Build+a+Habit+Tracker+Inspired+by+Atomic+Habits+-+slide2.png
                https://social-images-tylerai.s3.us-east-2.amazonaws.com/bolt-new/Build+a+Habit+Tracker+Inspired+by+Atomic+Habits+-+slide3.png
                https://social-images-tylerai.s3.us-east-2.amazonaws.com/bolt-new/Build+a+Habit+Tracker+Inspired+by+Atomic+Habits+-+slide4.png
                https://social-images-tylerai.s3.us-east-2.amazonaws.com/bolt-new/Build+a+Habit+Tracker+Inspired+by+Atomic+Habits+-+slide5.png
                https://social-images-tylerai.s3.us-east-2.amazonaws.com/bolt-new/Build+a+Habit+Tracker+Inspired+by+Atomic+Habits+-+slide6.png
                https://social-images-tylerai.s3.us-east-2.amazonaws.com/bolt-new/Build+a+Habit+Tracker+Inspired+by+Atomic+Habits+-+slide7.png
                
                Here is the order of operations:
                1. first upload the image urls to instagram (all of them)
                2. grab the media ids from each response
                3. then based on user input: {user_input}
                    - if carousel, then execute the upload_carousel_post tool with the caption and the list of media ids
                    - if single image publish, then publish the media id to instagram with caption
                4. once you have the container id from either single image or carousel publish, then execute the publish_media_container tool with the container id
                    - this actually publishes the post to instagram
            """,
            expected_output="A success message from the Instagram API",
            agent=instagram_agent,
            markdown=True
        )
        
        data_crew = Crew(
            agents=[instagram_agent],
            tasks=[processing_task],
            verbose=True,
            process=Process.sequential 
        )
    
        result = data_crew.kickoff()
        print("\nCrew Task Result (Stdio - Managed):\n", result)
    
if __name__ == "__main__":
    user_input = input("Enter type of post: ")
    main(user_input)