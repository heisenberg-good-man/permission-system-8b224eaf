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

class LoginRequest(BaseModel):
    email: str
    password: str

class Interview(BaseModel):
    id: Optional[int] = None
    resume_id: int
    job_id: int
    candidate_id: int
    candidate_name: str
    round: str
    interview_time: str
    method: str
    interviewer: str
    location: str
    remarks: str = ""
    status: str = "pending"
    cancel_reason: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Offer(BaseModel):
    id: Optional[int] = None
    resume_id: int
    job_id: int
    candidate_id: int
    candidate_name: str
    salary: str
    start_date: str
    work_location: str
    probation_period: str = ""
    department: str = ""
    notes: str = ""
    status: str = "draft"
    reject_reason: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class Feedback(BaseModel):
    id: Optional[int] = None
    interview_id: int
    resume_id: int
    job_id: int
    candidate_id: int
    candidate_name: str
    round: str
    interviewer: str
    score: int = 0
    tags: str = ""
    strengths: str = ""
    risks: str = ""
    conclusion: str = "pending"
    remarks: str = ""
    external_feedback: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

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

mock_interviews = [
    Interview(
        id=1,
        resume_id=2,
        job_id=1,
        candidate_id=4,
        candidate_name="赵六",
        round="初试",
        interview_time="2024-01-25 14:00",
        method="线上",
        interviewer="张三",
        location="腾讯会议",
        remarks="请提前准备自我介绍和项目经历",
        status="confirmed",
        created_at=datetime(2024, 1, 22, 15, 30),
        updated_at=datetime(2024, 1, 23, 10, 0)
    ),
]

mock_offers = [
    Offer(
        id=1,
        resume_id=2,
        job_id=1,
        candidate_id=4,
        candidate_name="赵六",
        salary="35k-45k",
        start_date="2024-02-01",
        work_location="北京",
        probation_period="3个月",
        department="技术部",
        notes="请在入职前完成体检",
        status="sent",
        created_at=datetime(2024, 1, 25, 10, 0),
        updated_at=datetime(2024, 1, 25, 11, 0)
    ),
]

mock_feedbacks = [
    Feedback(
        id=1,
        interview_id=1,
        resume_id=2,
        job_id=1,
        candidate_id=4,
        candidate_name="赵六",
        round="初试",
        interviewer="张三",
        score=85,
        tags="技术能力强,沟通流畅",
        strengths="React经验丰富，有大型项目经验",
        risks="薪资期望偏高",
        conclusion="pass",
        remarks="建议进入复试",
        external_feedback="",
        created_at=datetime(2024, 1, 25, 15, 0),
        updated_at=datetime(2024, 1, 25, 15, 30)
    ),
]

job_counter = 5
resume_counter = 4
message_counter = 5
interview_counter = 2
offer_counter = 2
feedback_counter = 2

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
def login(request: LoginRequest):
    user = next((u for u in mock_users if u.email == request.email), None)
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

@app.get("/api/interviews", response_model=List[Interview])
def get_interviews(
    recruiter_id: Optional[int] = Query(None),
    candidate_id: Optional[int] = Query(None),
    resume_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    date: Optional[str] = Query(None)
):
    result = mock_interviews
    if recruiter_id:
        result = [i for i in result if any(j.id == i.job_id and j.recruiter_id == recruiter_id for j in mock_jobs)]
    if candidate_id:
        result = [i for i in result if i.candidate_id == candidate_id]
    if resume_id:
        result = [i for i in result if i.resume_id == resume_id]
    if status:
        result = [i for i in result if i.status == status]
    if date:
        result = [i for i in result if i.interview_time.startswith(date)]
    return result

@app.get("/api/interviews/{interview_id}", response_model=Interview)
def get_interview(interview_id: int):
    interview = next((i for i in mock_interviews if i.id == interview_id), None)
    if not interview:
        raise HTTPException(status_code=404, detail="面试安排不存在")
    return interview

@app.post("/api/interviews", response_model=Interview)
def create_interview(interview: Interview):
    global interview_counter
    interview.id = interview_counter
    interview.created_at = datetime.now()
    interview.updated_at = datetime.now()
    mock_interviews.append(interview)
    interview_counter += 1
    return interview

@app.put("/api/interviews/{interview_id}", response_model=Interview)
def update_interview(interview_id: int, interview: Interview):
    index = next((i for i, r in enumerate(mock_interviews) if r.id == interview_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="面试安排不存在")
    interview.id = interview_id
    interview.created_at = mock_interviews[index].created_at
    interview.updated_at = datetime.now()
    mock_interviews[index] = interview
    return interview

@app.get("/api/offers", response_model=List[Offer])
def get_offers(
    recruiter_id: Optional[int] = Query(None),
    candidate_id: Optional[int] = Query(None),
    resume_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    job_id: Optional[int] = Query(None)
):
    result = mock_offers
    if recruiter_id:
        result = [o for o in result if any(j.id == o.job_id and j.recruiter_id == recruiter_id for j in mock_jobs)]
    if candidate_id:
        result = [o for o in result if o.candidate_id == candidate_id]
    if resume_id:
        result = [o for o in result if o.resume_id == resume_id]
    if status:
        result = [o for o in result if o.status == status]
    if job_id:
        result = [o for o in result if o.job_id == job_id]
    return result

@app.get("/api/offers/{offer_id}", response_model=Offer)
def get_offer(offer_id: int):
    offer = next((o for o in mock_offers if o.id == offer_id), None)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer不存在")
    return offer

@app.post("/api/offers", response_model=Offer)
def create_offer(offer: Offer):
    global offer_counter
    offer.id = offer_counter
    offer.created_at = datetime.now()
    offer.updated_at = datetime.now()
    mock_offers.append(offer)
    offer_counter += 1
    return offer

@app.put("/api/offers/{offer_id}", response_model=Offer)
def update_offer(offer_id: int, offer: Offer):
    index = next((i for i, o in enumerate(mock_offers) if o.id == offer_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="Offer不存在")
    offer.id = offer_id
    offer.created_at = mock_offers[index].created_at
    offer.updated_at = datetime.now()
    mock_offers[index] = offer
    return offer

@app.get("/api/feedbacks", response_model=List[Feedback])
def get_feedbacks(
    recruiter_id: Optional[int] = Query(None),
    candidate_id: Optional[int] = Query(None),
    resume_id: Optional[int] = Query(None),
    job_id: Optional[int] = Query(None),
    interview_id: Optional[int] = Query(None),
    conclusion: Optional[str] = Query(None),
    round: Optional[str] = Query(None)
):
    result = mock_feedbacks
    if recruiter_id:
        result = [f for f in result if any(j.id == f.job_id and j.recruiter_id == recruiter_id for j in mock_jobs)]
    if candidate_id:
        result = [f for f in result if f.candidate_id == candidate_id]
    if resume_id:
        result = [f for f in result if f.resume_id == resume_id]
    if job_id:
        result = [f for f in result if f.job_id == job_id]
    if interview_id:
        result = [f for f in result if f.interview_id == interview_id]
    if conclusion:
        result = [f for f in result if f.conclusion == conclusion]
    if round:
        result = [f for f in result if f.round == round]
    return result

@app.get("/api/feedbacks/{feedback_id}", response_model=Feedback)
def get_feedback(feedback_id: int):
    feedback = next((f for f in mock_feedbacks if f.id == feedback_id), None)
    if not feedback:
        raise HTTPException(status_code=404, detail="面试反馈不存在")
    return feedback

@app.post("/api/feedbacks", response_model=Feedback)
def create_feedback(feedback: Feedback):
    global feedback_counter
    feedback.id = feedback_counter
    feedback.created_at = datetime.now()
    feedback.updated_at = datetime.now()
    mock_feedbacks.append(feedback)
    
    if feedback.conclusion in ["pass", "next_round"]:
        resume_index = next((i for i, r in enumerate(mock_resumes) if r.id == feedback.resume_id), None)
        if resume_index is not None:
            mock_resumes[resume_index].status = "interview"
            mock_resumes[resume_index].updated_at = datetime.now()
    elif feedback.conclusion == "reject":
        resume_index = next((i for i, r in enumerate(mock_resumes) if r.id == feedback.resume_id), None)
        if resume_index is not None:
            mock_resumes[resume_index].status = "rejected"
            mock_resumes[resume_index].updated_at = datetime.now()
    
    feedback_counter += 1
    return feedback

@app.put("/api/feedbacks/{feedback_id}", response_model=Feedback)
def update_feedback(feedback_id: int, feedback: Feedback):
    index = next((i for i, f in enumerate(mock_feedbacks) if f.id == feedback_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="面试反馈不存在")
    
    old_conclusion = mock_feedbacks[index].conclusion
    feedback.id = feedback_id
    feedback.created_at = mock_feedbacks[index].created_at
    feedback.updated_at = datetime.now()
    mock_feedbacks[index] = feedback
    
    if feedback.conclusion in ["pass", "next_round"]:
        resume_index = next((i for i, r in enumerate(mock_resumes) if r.id == feedback.resume_id), None)
        if resume_index is not None:
            mock_resumes[resume_index].status = "interview"
            mock_resumes[resume_index].updated_at = datetime.now()
    elif feedback.conclusion == "reject":
        resume_index = next((i for i, r in enumerate(mock_resumes) if r.id == feedback.resume_id), None)
        if resume_index is not None:
            mock_resumes[resume_index].status = "rejected"
            mock_resumes[resume_index].updated_at = datetime.now()
    
    return feedback

@app.delete("/api/feedbacks/{feedback_id}")
def delete_feedback(feedback_id: int):
    global mock_feedbacks
    index = next((i for i, f in enumerate(mock_feedbacks) if f.id == feedback_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="面试反馈不存在")
    mock_feedbacks.pop(index)
    return {"message": "删除成功"}

@app.get("/api/stats/{user_id}")
def get_stats(user_id: int):
    user = next((u for u in mock_users if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    if user.role == "recruiter":
        jobs_count = len([j for j in mock_jobs if j.recruiter_id == user_id])
        resumes_count = len([r for r in mock_resumes if any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs)])
        pending_count = len([r for r in mock_resumes if any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) and r.status == "pending"])
        interview_count = len([r for r in mock_resumes if any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) and r.status == "interview"])
        my_interviews = [i for i in mock_interviews if any(j.id == i.job_id and j.recruiter_id == user_id for j in mock_jobs)]
        pending_interview_count = len([i for i in my_interviews if i.status == "pending"])
        today_interview_count = len([i for i in my_interviews if i.interview_time.startswith(today_str)])
        completed_interview_count = len([i for i in my_interviews if i.status == "completed"])
        my_offers = [o for o in mock_offers if any(j.id == o.job_id and j.recruiter_id == user_id for j in mock_jobs)]
        draft_offer_count = len([o for o in my_offers if o.status == "draft"])
        sent_offer_count = len([o for o in my_offers if o.status == "sent"])
        accepted_offer_count = len([o for o in my_offers if o.status == "accepted"])
        rejected_offer_count = len([o for o in my_offers if o.status == "rejected"])
    else:
        jobs_count = len(mock_jobs)
        resumes_count = len([r for r in mock_resumes if r.candidate_id == user_id])
        pending_count = len([r for r in mock_resumes if r.candidate_id == user_id and r.status == "pending"])
        interview_count = len([r for r in mock_resumes if r.candidate_id == user_id and r.status == "interview"])
        my_interviews = [i for i in mock_interviews if i.candidate_id == user_id]
        pending_interview_count = len([i for i in my_interviews if i.status == "pending"])
        today_interview_count = len([i for i in my_interviews if i.interview_time.startswith(today_str)])
        completed_interview_count = len([i for i in my_interviews if i.status == "completed"])
        my_offers = [o for o in mock_offers if o.candidate_id == user_id]
        draft_offer_count = len([o for o in my_offers if o.status == "draft"])
        sent_offer_count = len([o for o in my_offers if o.status == "sent"])
        accepted_offer_count = len([o for o in my_offers if o.status == "accepted"])
        rejected_offer_count = len([o for o in my_offers if o.status == "rejected"])
    
    return {
        "jobs_count": jobs_count,
        "resumes_count": resumes_count,
        "pending_count": pending_count,
        "interview_count": interview_count,
        "rejected_count": len([r for r in mock_resumes if (user.role == "recruiter" and any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) or user.role == "candidate" and r.candidate_id == user_id) and r.status == "rejected"]),
        "applied_count": len([r for r in mock_resumes if (user.role == "recruiter" and any(j.id == r.job_id and j.recruiter_id == user_id for j in mock_jobs) or user.role == "candidate" and r.candidate_id == user_id) and r.status == "applied"]),
        "pending_interview_count": pending_interview_count,
        "today_interview_count": today_interview_count,
        "completed_interview_count": completed_interview_count,
        "draft_offer_count": draft_offer_count,
        "sent_offer_count": sent_offer_count,
        "accepted_offer_count": accepted_offer_count,
        "rejected_offer_count": rejected_offer_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)