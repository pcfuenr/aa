# 🏋️‍♂️ Workout Tracker - Full Stack Application

A full-stack workout tracking application that helps users manage their fitness journey with detailed workout logging, exercise management, and progress tracking. 

## 🌟 Overview

This application consists of FastAPI backend with a React TypeScript frontend, providing a complete solution for personal fitness tracking and gym management.

### ✨ Key Features

**👤 For Users:**
- 🔐 Secure authentication and profile management
- 🏃‍♂️ Interactive workout session tracking
- 📊 Detailed exercise logging with sets, reps, weights, and duration
- 📈 Workout history
- 📝 Workout and exercise notes
- 📋 Pre-built workout templates
- 📱 Responsive design for mobile and desktop

**👨‍💼 For Administrators:**
- 👥 Complete user management system
- 💪 Exercise database administration
- 📋 Workout template creation and management
- 🛡️ Role-based access control

## 🏗️ Architecture

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend** | FastAPI + SQLAlchemy | REST API with ORM database access |
| **Frontend** | React 19 + TypeScript | Modern SPA with type safety |
| **Database** | PostgreSQL | Reliable relational data storage |
| **Styling** | Tailwind CSS 4.x | Utility-first responsive design |
| **Authentication** | JWT Tokens | Secure stateless authentication |
| **Build Tools** | Vite + ESLint | Fast development and quality assurance |


## 🚀 Quick Start
Check the readme in workouts_udec_backend and workouts_udec_frontend to get started.

## 🐳 Docker Setup
This section guides you through using Docker to build and run the entire application stack.

<h3>Prerrequisitos</h3>
<ul>
  <li><a href="https://www.docker.com/get-started" target="_blank">Docker</a></li>
  <li><a href="https://docs.docker.com/compose/install/" target="_blank">Docker Compose</a></li>
</ul>


### ▶️ Build and Run the Application
The `docker-compose.yaml` file in the project root directory defines all the services needed to run the application.
```bash
docker-compose up --build
```
This command will initialize all the services defined in `docker-compose.yaml`.

<p>Once the containers are running, you can access the application at the following addresses:</p>
<ul>
<li>
<strong>Frontend:</strong>
<a href="http://localhost:4173/">http://localhost:4173/</a>
</li>
<li>
<strong>Backend (API):</strong>
<a href="http://localhost:8000/docs">http://localhost:8000/docs</a> (interactive API documentation, Swagger UI)
</li>
</ul>

### 🛑Stop and Cleanup
To stop services without removing them, use:

```bash
docker-compose stop
```
<p>To stop and remove all containers, networks, and volumes defined in the <code>docker-compose.yaml</code> file, use the following command:

<pre><code class="language-bash">docker-compose down -v</code></pre>

<h3>💻 More useful Docker commands</h3>
<p>
These commands will help you manage your application's services efficiently while working on your project.
</p>
<ul>
<li>
<strong>View running containers:</strong>
<p>
This command displays a list of all currently running containers. It's useful for checking the status of your services.
</p>
<pre><code class="language-bash">docker ps</code></pre>
</li>
<li>
<strong>View logs for all services:</strong>
<p>
Use this command to view the combined log output of all containers defined in your <code>docker-compose.yaml</code> file.
</p>
<pre><code class="language-bash">docker-compose logs</code></pre>
</li>
</ul>
<ul>
<li>
<strong>Docker Documentation:</strong>
<p>Learn about all Docker commands, container architecture, and best practices.</p>
<pre><code class="language-bash">docker --help</code></pre>
<p>Visit the official site:     <a href="https://docs.docker.com/"target="_blank">Docker Docs</a>
</p>
</li>
<li>
<strong>Docker Compose Documentation:</strong>
<p>Find information on defining and managing multi-container applications.</p>
<pre><code class="language-bash">docker-compose --help</code></pre>
<p>Visit the official site:     <a href="https://docs.docker.com/compose/" target="_blank">Docker Compose Docs</a>

</p>
</li>
</ul>

<h3>💹 Static Analysis commands</h3>
<p>
These are the commands for the static analysis tools.
</p>
<ul>
<li>
<strong>Run Pylint analysis:</strong>
<p>
Displays a list that shows issues with style, mistakes and conventions
</p>
<pre><code class="language-bash">docker compose exec backend pylint app/</code></pre>
</li>
<li>
<strong>Run Bandit analysis:</strong>
<p>
Displays the security issues
</p>
<pre><code class="language-bash">docker compose exec backend bandit -r app/</code></pre>
</li>
<li>
<strong>Run Radon analysis:</strong>
<p>
Displays a list with the ciclomatic complexity
</p>
<pre><code class="language-bash">docker compose exec backend radon cc -s app/</code></pre>
</li>
</ul>

<h3>✅ Run tests with newman</h3>
<p>
Newman automatically runs when the <code>docker-compose up --build</code> command is executed
<p>
It shows a list of every test and their respective code
</p>
</p>

<div align="right">
    <a href="https://www.docker.com/" target="_blank">
        <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    </a>
    <a href="https://opensource.org/licenses/MIT" target="_blank">
        <img src="https://img.shields.io/badge/license-MIT-informational?style=for-the-badge" alt="License">
    </a>
</div>

### TESTS

Para usar los tests se debe de abrir la aplicación de postman, e importar los archivos json de la carpeta tests/postman.


<img width="494" height="73" alt="image" src="https://github.com/user-attachments/assets/cb88648b-62b8-4150-acb9-4b52e7ed0dc5" />

Los archivos relevantes son los 3 Endpoints-Casos....
y los 3 Workout-Api que son los enviroment.

Posteriormente para cada test asignar su enviroment correspondiente en la esquina superior derecha


<img width="1447" height="387" alt="image" src="https://github.com/user-attachments/assets/5d5726cf-d728-425d-8f70-adff44a95983" />

y finalmente darle click derecho a cada collection, luego darle click a run


<img width="553" height="672" alt="image" src="https://github.com/user-attachments/assets/1e6fb32d-89e5-48f7-a3c2-5b9b6720190b" />

Por ultimo darle a Run Endpoints Casos positivos


<img width="578" height="812" alt="image" src="https://github.com/user-attachments/assets/60d27738-4959-41c5-8b17-5279df35d825" />
