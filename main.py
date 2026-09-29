from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from database import engine, Base
from models.user import User
from models.recommendation import Recommendation

from routes.auth import router as auth_router
from routes.home import router as home_router
from routes.party import router as party_router
from routes.jewelry import router as jewelry_router
from routes.history import router as history_router


Base.metadata.create_all(bind=engine)


app = FastAPI(title="PocketSmart AI")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    SessionMiddleware,
    secret_key="pocketsmart-secret-key-change-later"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(home_router)
app.include_router(party_router)
app.include_router(jewelry_router)
app.include_router(history_router)


@app.get("/", response_class=HTMLResponse)
def landing_page():
    return """
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <title>PocketSmart AI</title>

        <style>

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: Arial, sans-serif;
                min-height: 100vh;
                background: linear-gradient(135deg, #eef2ff, #f8f9ff);
                color: #222;
            }

            .navbar {
                background: white;
                padding: 18px 50px;

                display: flex;
                justify-content: space-between;
                align-items: center;

                box-shadow: 0 2px 15px rgba(0,0,0,0.08);
            }

            .logo {
                font-size: 24px;
                font-weight: bold;
                color: #5b4bdb;
            }

            .login {
                text-decoration: none;
                color: #5b4bdb;
                font-weight: bold;
            }

            .hero {
                max-width: 1100px;
                margin: 70px auto 45px;
                padding: 0 25px;

                display: grid;
                grid-template-columns: 1.2fr 0.8fr;
                gap: 50px;
                align-items: center;
            }

            .hero-content h1 {
                font-size: 52px;
                line-height: 1.1;
                margin-bottom: 20px;
            }

            .highlight {
                color: #5b4bdb;
            }

            .hero-content p {
                font-size: 18px;
                line-height: 1.7;
                color: #666;
                margin-bottom: 28px;
            }

            .buttons {
                display: flex;
                gap: 14px;
                flex-wrap: wrap;
            }

            .button {
                display: inline-block;
                padding: 14px 24px;
                border-radius: 11px;
                text-decoration: none;
                font-weight: bold;
            }

            .primary {
                background: #5b4bdb;
                color: white;
            }

            .primary:hover {
                background: #4939c7;
            }

            .secondary {
                background: white;
                color: #5b4bdb;
                border: 1px solid #ddd;
            }

            .hero-card {
                background: white;
                padding: 35px;
                border-radius: 25px;

                box-shadow: 0 10px 35px rgba(0,0,0,0.09);

                text-align: center;
            }

            .hero-icon {
                font-size: 85px;
                margin-bottom: 20px;
            }

            .hero-card h2 {
                margin-bottom: 12px;
            }

            .hero-card p {
                color: #666;
                line-height: 1.6;
            }

            .features {
                max-width: 1100px;
                margin: 20px auto 60px;
                padding: 0 25px;
            }

            .features h2 {
                text-align: center;
                font-size: 30px;
                margin-bottom: 25px;
            }

            .cards {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 22px;
            }

            .card {
                background: white;
                padding: 28px;
                border-radius: 20px;

                box-shadow: 0 6px 22px rgba(0,0,0,0.07);

                text-align: center;
            }

            .card-icon {
                font-size: 45px;
                margin-bottom: 15px;
            }

            .card h3 {
                font-size: 20px;
                margin-bottom: 10px;
            }

            .card p {
                color: #666;
                line-height: 1.5;
            }

            .footer {
                text-align: center;
                padding: 25px;
                color: #777;
                font-size: 13px;
            }

            @media (max-width: 800px) {

                .navbar {
                    padding: 18px 25px;
                }

                .hero {
                    grid-template-columns: 1fr;
                    text-align: center;
                    margin-top: 45px;
                }

                .hero-content h1 {
                    font-size: 40px;
                }

                .buttons {
                    justify-content: center;
                }

                .cards {
                    grid-template-columns: 1fr;
                }

            }

        </style>

    </head>


    <body>

        <div class="navbar">

            <div class="logo">
                💰 PocketSmart AI
            </div>

        <div>
            <a class="login" href="/testimonials">
                 Testimonials
            </a>

            <a class="login" href="/login" style="margin-left: 20px;">
                 Login →
            </a>
        </div>

        </div>


        <section class="hero">

            <div class="hero-content">

                <h1>
                    Plan Smarter with
                    <span class="highlight">AI</span>
                </h1>

                <p>
                    PocketSmart AI helps you plan your budget and
                    get practical recommendations for your home,
                    parties and jewelry.
                </p>

                <div class="buttons">

                    <a class="button primary" href="/register">
                        Get Started →
                    </a>

                    <a class="button secondary" href="/login">
                        Login
                    </a>

                </div>

            </div>


            <div class="hero-card">

                <div class="hero-icon">
                    🤖💰
                </div>

                <h2>
                    Your Smart Budget Assistant
                </h2>

                <p>
                    Enter your budget and requirements,
                    and PocketSmart AI creates a practical
                    recommendation for you.
                </p>

            </div>

        </section>


        <section class="features">

            <h2>
                What Can You Plan?
            </h2>


            <div class="cards">

                <div class="card">

                    <div class="card-icon">
                        🏠
                    </div>

                    <h3>
                        Home Planner
                    </h3>

                    <p>
                        Plan your home shopping and
                        interior requirements according
                        to your budget.
                    </p>

                </div>


                <div class="card">

                    <div class="card-icon">
                        🎉
                    </div>

                    <h3>
                        Party Planner
                    </h3>

                    <p>
                        Create a practical party plan
                        for catering, decoration and
                        entertainment.
                    </p>

                </div>


                <div class="card">

                    <div class="card-icon">
                        💍
                    </div>

                    <h3>
                        Jewelry Planner
                    </h3>

                    <p>
                        Get jewelry suggestions based
                        on your budget, occasion and
                        personal style.
                    </p>

                </div>

            </div>

        </section>


        <div class="footer">

            © 2026 PocketSmart AI · Smart Budget & Recommendation Assistant

        </div>

    </body>

    </html>
    """
templates = Jinja2Templates(directory="templates")


@app.get("/testimonials")
def testimonials(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="testimonials.html",
        context={}
    )
@app.get("/startup")
def startup():
    return {
        "status": "PocketSmart AI is running",
        "message": "Application services and configuration loaded successfully"
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )