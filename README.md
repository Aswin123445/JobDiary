# Job Diary - AI-Powered Job Application Tracker

## Overview

Job hunting can be overwhelming, especially when you submit 60+ applications and struggle to keep track of follow-ups, interview calls, and your research notes for each company. Job Diary helps you stay organized by storing all your job applications and detailed company/job research in one place.

With Job Diary, you can also generate AI-powered summaries of your research on demand — so you have quick, concise reports to review before interviews or follow-ups. Plus, automated email reminders help you never miss a follow-up for pending applications.

The app features secure email-based authentication using Authlib, and uses the Groq API for smart AI-generated summaries.

---

## Key Features

- Submit and manage unlimited job applications  
- Store detailed research notes about companies and job roles  
- Receive automated email reminders for applications pending over 10 days  
- Generate professional AI summaries of job and company research  
- Export AI summaries as well-formatted PDF reports  
- Secure authentication with email sign-in and registration via Authlib  
- Built with FastAPI, SQLModel, and async Python for speed and scalability

---

## Getting Started

### Prerequisites

- Python 3.10 or higher  
- PostgreSQL database  
- [Grok API key](https://grok.ai) for AI summary generation  
- Environment to run FastAPI app (local or server)

### Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/Aswin123445/job-diary.git
   cd job-diary
