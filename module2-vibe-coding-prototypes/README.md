# AI-Powered Coding: From Prompts to Project Planning &lt;packt&gt;

## Module 2: Vibe Coding for Prototyping
[https://www.coursera.org/learn/packt-ai-powered-coding-from-prompts-to-project-planning-8wtpj/lecture/yeIcn/prompt-assignment](https://www.coursera.org/learn/packt-ai-powered-coding-from-prompts-to-project-planning-8wtpj/lecture/yeIcn/prompt-assignment)

### Exercise 1: Landing Page Prompt

Using browser [https://claude.ai/new](https://claude.ai/new)

    Write a prompt to generate a landing page using principles from previous
    lessons in course.  Pick any SaaS product you want & design a prompt to spec:
    
      * what specific sections & content you need
      * what tech reqs should be used (since claude, prob just HTML, CSS, vanilla JS)
      * what design direction or references can you give it for UI?
      * be specific enough that AI is not guessing

```txt
Create a landing page for "Yotta Roots" - a genealogical platform for professional &
serious amateur genealogists sick of the noise of popular platforms.

SECTIONS:
  - Hero with headline, subheading, CTA, and example screenshot showing a
    family tree with a modal for editing a person's details open in front of it 
  - Summary of four primary Features:
    - Own Your Own Data, and who you share it with
    - Community, via federated micro-social networking with other researchers
    - Versioned, experiment with alternate histories without destroying data
    - Empowering, fully extensible and based on free & open source software
  - Pricing Models
    - Fully hosted, fully isolated, no limits
    - Community Edition
  - Who We Are
    - Founder, with 3 decades web & data engineering expertise, and 25 years
      involvement with Free Software & Data Privacy groups
    - Community, tech-minded amateur genealogists who want to build solutions
      that empower users to own their own data and services, not another
      platform holding your data hostage for a fee
  - Footer with links

TECHNICAL:
  - HTML with vanilla CSS & minimal JS
  - Smooth scroll navigation
  - Mobile responsive
  - Gradient background in hero

DESIGN:
  - Lean toward grassroots design aesthetic, not corporate
  - We are serious researchers who take library science and engineering
    seriously
  - Clean, modern typography
  - Dark mode friendly
  - Earth colors for logos, green, brown, possibly pale/sky blue for area
    backgrounds

Include sample content
Make all buttons functional (scroll to sections)
```

### Exercise 2: Prompt Assignment

Using browser [v0.app](v0.app)

Copy template from
[https://github.com/kennethd/coding-with-ai-course-resources/blob/main/prompts/prototype-example-prompts.md#template](https://github.com/kennethd/coding-with-ai-course-resources/blob/main/prompts/prototype-example-prompts.md#template)

Sample vibe coding prompt:
```txt
I want to prototype a markdown note-taking app in React.

Here are the requirements:

FEATURES:
- Create, edit and delete notes
- Live markdown preview (editor on left, preview on right)
- Auto save to local storage with debouncing
- Sidebar with all notes showing title and date
- Search functionality to filter notes
- Dark/light mode toggle


TECHNICAL REQUIREMENTS:
- Use react with functional components and hooks
- Use react-markdown for preview rendering
- Responsive design
- Clean modern UI with Tailwind v4

STRUCTURE:
- Break UI into separate components where it makes sense
```

Review:

  * Security Concerns
  * File/component structure
  * State mgmt
  * Error handling
  * Dead code, unused imports
  * Dependencies
  * What got right/wrong
  * Overengineering



