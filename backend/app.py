from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="招聘平台 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Job(BaseModel):
    id: Optional[int] = None
    title: str
    company: str
    location: str
    salary: str
    experience: str
    education: str
    description: str
    recruiter_id: int
    created_at: Optional[datetime] = None
    status: str = "active"

class Resume(BaseModel):
    id: Optional[int] = None
    job_id: int
    candidate_id: int
    candidate_name: str
    phone: str
    email: str
    education: str
    experience: str
    skills: str
    resume_text: str
    status: str = "applied"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Message(BaseModel):
    id: Optional[int] = None
    resume_id: int
    sender_id: int
    sender_role: str
    content: str
    created_at: Optional[datetime] = None

class User(BaseModel):
    id: int
    name: str
    role: str
    email: str

mock_users = [
    User(id=1, name="张三", role="recruiter", email="zhangsan@company.com"),
    User(id=2, name="李四", role="candidate", email="lisi@example.com"),
    User(id=3, name="王五", role="recruiter", email="wangwu@company.com"),
    User(id=4, name="赵六", role="candidate", email="zhaoliu@example.com"),
]

mock_jobs = [
    Job(
        id=1,
        title="高级前端工程师",
        company="字节跳动",
        location="北京",
        salary="25k-45k",
        experience="3-5年",
        education="本科",
        description="负责公司核心产品的前端开发，要求精通Vue/React，有大型项目经验。",
        recruiter_id=1,
        created_at=datetime(2024, 1, 15, 10, 30),
        status="active"
    ),
    Job(
        id=2,
        title="Python后端开发",
        company="阿里巴巴",
        location="杭州",
        salary="30k-50k",
        experience="3-5年",
        education="本科",
        description="负责后端服务开发，熟悉Django/FastAPI，有微服务经验优先。",
        recruiter_id=1,
        created_at=datetime(2024, 1, 10, 9, 0),
        status="active"
    ),
    Job(
        id=3,
        title="产品经理",
        company="腾讯",
        location="深圳",
        salary="20k-40k",
        experience="2-4年",
        education="本科",
        description="负责产品规划和需求分析，有互联网产品经验。",
        recruiter_id=3,
        created_at=datetime(2024, 1, 5, 14, 20),
        status="active"
    ),
    Job(
        id=4,
        title="UI设计师",
        company="美团",
        location="北京",
        salary="15k-30k",
        experience="2-3年",
        education="大专",
        description="负责产品界面设计，精通Figma/Sketch，有用户体验意识。",
        recruiter_id=3,
        created_at=datetime(2024, 1, 8, 11, 15),
        status="active"
    ),
]

mock_resumes = [
    Resume(
        id=1,
        job_id=1,
        candidate_id=2,
        candidate_name="李四",
        phone="13800138001",
        email="lisi@example.com",
        education="本科",
        experience="4年",
        skills="Vue, React, TypeScript",
        resume_text="我有4年前端开发经验，曾在多家互联网公司工作...",
        status="pending",
        created_at=datetime(2024, 1, 20, 16, 45),
        updated_at=datetime(2024, 1, 21, 10, 0)
    ),
    Resume(
        id=2,
        job_id=1,
        candidate_id=4,
        candidate_name="赵六",
        phone="13800138002",
        email="zhaoliu@example.com",
        education="硕士",
        experience="3年",
        skills="React, Node.js, GraphQL",
        resume_text="3年前端经验，专注于用户体验优化...",
        status="interview",
        created_at=datetime(2024, 1, 18, 9, 30),
        updated_at=datetime(2024, 1, 22, 14, 30)
    ),
    Resume(
        id=3,
        job_id=2,
        candidate_id=2,
        candidate_name="李四",
        phone="13800138001",
        email="lisi@example.com",
        education="本科",
        experience="4年",
        skills="Python, Django, FastAPI",
        resume_text="全栈开发经验，熟悉Python生态...",
        status="applied",
        created_at=datetime(2024, 1, 22, 15, 0),
        updated_at=datetime(2024, 1, 22, 15, 0)
    ),
]

mock_messages = [
    Message(
        id=1,
        resume_id=1,
        sender_id=2,
        sender_role="candidate",
        content="您好，我对这个职位很感兴趣，希望能有机会面试！",
        created_at=datetime(2024, 1, 20, 16, 50)
    ),
    Message(
        id=2,
        resume_id=1,
        sender_id=1,
        sender_role="recruiter",
        content="收到您的简历，我们会尽快评估，有消息会通知您。",
        created_at=datetime(2024, 1, 21, 10, 15)
    ),
    Message(
        id=3,
        resume_id=2,
        sender_id=1,
        sender_role="recruiter",
        content="您好，我们对您的背景很感兴趣，请问本周三下午方便面试吗？",
        created_at=datetime(2024, 1, 22, 14, 35)
    ),
    Message(
        id=4,
        resume_id=2,
        sender_id=4,
        sender_role="candidate",
        content="周三下午可以的，请问具体时间和地点？",
        created_at=datetime(2024, 1, 22, 15, 0)
    ),
]

job_counter = 5
resume_counter = 4
message_counter = 5

@app.get("/api/users", response_model=List[User])
def get_users(role: Optional[str] = Query(None)):
    if role:
        return [u for u in mock_users if u.role == role]
    return mock_users

@app.get("/api/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in mock_users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.post("/api/users/login")
def login(email: str, password: str):
    user = next((u for u in mock_users if u.email == email), None)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    return {"user": user, "token": f"token_{user.id}"}

@app.get("/api/jobs", response_model=List[Job])
def get_jobs(recruiter_id: Optional[int] = Query(None), status: Optional[str] = Query(None)):
    result = mock_jobs
    if recruiter_id:
        result = [j for j in result if j.recruiter_id == recruiter_id]
    if status:
        result = [j for j in result if j.status == status]
    return result

@app.get("/api/jobs/{job_id}", response_model=Job)
def get_job(job_id: int):
    job = next((j for j in mock_jobs if j.id == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="职位不存在")
    return job

@app.post("/api/jobs", response_model=Job)
def create_job(job: Job):
    global job_counter
    job.id = job_counter
    job.created_at = datetime.now()
    mock_jobs.append(job)
    job_counter += 1
    return job

@app.put("/api/jobs/{job_id}", response_model=Job)
def update_job(job_id: int, job: Job):
    index = next((i for i, j in enumerate(mock_jobs) if j.id == job_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="职位不存在")
    job.id = job_id
    job.created_at = mock_jobs[index].created_at
    mock_jobs[index] = job
    return job

@app.delete("/api/jobs/{job_id}")
def delete_job(job_id: int):
    global mock_jobs
    index = next((i for i, j in enumerate(mock_jobs) if j.id == job_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="职位不存在")
    mock_jobs.pop(index)
    return {"message": "删除成功"}

@app.get("/api/resumes", response_model=List[Resume])
def get_resumes(job_id: Optional[int] = Query(None), candidate_id: Optional[int] = Query(None), status: Optional[str] = Query(None)):
    result = mock_resumes
    if job_id:
        result = [r for r in result if r.job_id == job_id]
    if candidate_id:
        result = [r for r in result if r.candidate_id == candidate_id]
    if status:
        result = [r for r in result if r.status == status]
    return result

@app.get("/api/resumes/{resume_id}", response_model=Resume)
def get_resume(resume_id: int):
    resume = next((r for r in mock_resumes if r.id == resume_id), None)
    if not resume:
        raise HTTPException(status_code=404, detail="简历不存在")
    return resume

@app.post("/api/resumes", response_model=Resume)
def create_resume(resume: Resume):
    global resume_counter
    resume.id = resume_counter
    resume.created_at = datetime.now()
    resume.updated_at = datetime.now()
    mock_resumes.append(resume)
    resume_counter += 1
    return resume

@app.put("/api/resumes/{resume_id}", response_model=Resume)
def update_resume(resume_id: int, resume: Resume):
    index = next((i for i, r in enumerate(mock_resumes) if r.id == resume_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="简历不存在")
    resume.id = resume_id
    resume.created_at = mock_resumes[index].created_at
    resume.updated_at = datetime.now()
    mock_resumes[index] = resume
    return resume

@app.get("/api/messages", response_model=List[Message])
def get_messages(resume_id: int):
    return [m for m in mock_messages if m.resume_id == resume_id]

@app.post("/api/messages", response_model=Message)
def create_message(message: Message):
    global message_counter
    message.id = message_counter
    message.created_at = datetime.now()
    mock_messages.append(message)
    message_counter += 1
    return message

@app.get("/api/stats/{user_id}")
def get_stats(user_id: int):
    user = next((u for u in mock_users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.role == "recruiter":
        jobs_count = len([j for j in mock_jobs if j.recruiter_id == user_id])
        resumes_count = len([r for r in mock_resumes if any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs)])
        pending_count = len([r for r in mock_resumes if any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) and r.status == "pending"])
        interview_count = len([r for r in mock_resumes if any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) and r.status == "interview"])
    else:
        jobs_count = len(mock_jobs)
        resumes_count = len([r for r in mock_resumes if r.candidate_id == user_id])
        pending_count = len([r for r in mock_resumes if r.candidate_id == user_id and r.status == "pending"])
        interview_count = len([r for r in mock_resumes if r.candidate_id == user_id and r.status == "interview"])
    
    return {
        "jobs_count": jobs_count,
        "resumes_count": resumes_count,
        "pending_count": pending_count,
        "interview_count": interview_count,
        "rejected_count": len([r for r in mock_resumes if (user.role == "recruiter" and any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) or user.role == "candidate" and r.candidate_id == user_id) and r.status == "rejected"]),
        "applied_count": len([r for r in mock_resumes if (user.role == "recruiter" and any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) or user.role == "candidate" and r.candidate_id == user_id) and r.status == "applied"])
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)