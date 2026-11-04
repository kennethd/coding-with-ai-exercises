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




### Exercise 1 v2: Landing Page Prompt

Using claude 2.1.318 (Claude Code)

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
  - Why? Section (but with a better title)
    - The LDS project and major sites like Ancestry are founded on an idea of
      creating a massive genealogical record of all of humanity.  To us, this
      seems misguided, data is imported into and shared from each instance
      only about families represented in the trees hosted there
    - Less noise.  My god I must have tens of thousands of hints the major
      sites want me to review based on vaguely similar names
    - Control of your network, only connect your network to researchers you
      trust
    - Confidence Scores.  All data and relationships are weighted with
      confidence scores
  - Screenshots
    - Map of locations in US and world tracking the history of a family branch
    - Prioritized TODO lists, ex:
      - Next Time in New Haven: photograph headstone at Grove St. Cemetary,
        look up colonial records at public archives, etc
    - Calendar of past events, Today is your Great-Great-Great-Grandmother's birthday, etc
  - Detail section for each of the 4 primary features with following emphasis,
    including one illustrative graphic per feature
    - Community
      - Every instance is a micro-social network hub connected to researchers
        with interest in the same family
      - Built-in social platform doubles as a family Mastodon server, fully
        integrated with the Fediverse
    - Versioned trees
      - Create experimental branches when the data gets fuzzy
      - Rollback changes when you realize you've strayed down the wrong path
    - Data Ownership & Privacy (illustration should emphasize protection from
      evil data brokers)
      - All data is exportable in a variety of standard and archival formats
      - Yotta Roots will never share data or do business with data brokers
    - Empowering (illustration should include Docker whale)
      - Built on the FadoDevStack Docker Swarm-based open source self-hosting
        infrastructure platform, including
  - Pricing Models
    - Fully hosted, fully isolated, no limits
    - Shared hosting, 
    - Community Edition, self-host the open source core, may lag behind in
      features
  - Who We Are
    - Founder, with 3 decades web & data engineering expertise, and 25 years
      involvement with Free Software & Data Privacy groups
    - Community, tech-minded amateur genealogists who want to build solutions
      that empower users to own their own data and services, not another
      platform holding your data hostage for a fee
  - Footer with links

TECHNICAL:
  - HTML with vanilla CSS & minimal JS, no major frameworks
  - Smooth scroll navigation
  - Mobile responsive
  - Gradient background in hero

DESIGN:
  - Lean toward grassroots design aesthetic, not corporate
  - We are serious researchers who take library science and engineering seriously
  - Clean, modern typography
  - Dark mode friendly
  - Earth colors for logos, green, brown, possibly pale/sky blue for area backgrounds

Include sample content
Make all buttons functional (scroll to sections)
```

