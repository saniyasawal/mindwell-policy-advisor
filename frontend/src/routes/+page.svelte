
<script>
  import { marked } from 'marked';

  let renderedAnswer = '';

  let question = 'Should colleges in India introduce optional mindfulness and stress-management sessions for students?';
  let population = 'Students and young adults';
  let context = 'India';
  let loading = false;
  let error = '';
  let result = null;

  const examples = [
    'Should colleges in India introduce optional mindfulness and stress-management sessions for students?',
    'How can employers reduce stress while improving access to counselling?',
    'Compare school wellbeing education with expanding access to qualified counsellors.'
  ];

  async function analyse() {
    loading = true;
    error = '';
    result = null;
    renderedAnswer = '';

    try {
      const r = await fetch('http://127.0.0.1:8000/api/policy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          question,
          population,
          context
        })
      });

      const d = await r.json();

      if (!r.ok) {
        throw new Error(d.detail || 'Request failed');
      }

      result = d;

      // Convert Markdown to HTML and sanitize it before rendering.
      const html = await marked.parse(d.answer || '');
      const DOMPurify = (await import('dompurify')).default;
      renderedAnswer = DOMPurify.sanitize(html);
    } catch (e) {
      error = e.message || 'Could not connect to backend.';
    } finally {
      loading = false;
    }
  }
</script>

<svelte:head>
  <title>MindWell Policy Advisor</title>
  <meta
    name="description"
    content="Evidence-aware public wellbeing policy analysis"
  />
</svelte:head>

<div class="page">
  <header>
    <div class="eyebrow">AGENTIC AI · POLICY ANALYSIS</div>
    <h1>MindWell <span>Policy Advisor</span></h1>
    <p class="sub">
      Evidence-aware recommendations for public wellbeing, with implementation
      plans and trade-offs.
    </p>
  </header>

  <main>
    <section class="panel">
      <div class="eyebrow">01 / POLICY QUESTION</div>
      <h2>Define the policy question</h2>
      <p class="muted">
        Describe the public decision you want to evaluate.
      </p>

      <label for="q">Policy question</label>
      <textarea id="q" bind:value={question} rows="4"></textarea>

      <div class="twocol">
        <div>
          <label for="p">Target population</label>
          <select id="p" bind:value={population}>
            <option>Students and young adults</option>
            <option>School students and teachers</option>
            <option>Employees and managers</option>
            <option>General public</option>
            <option>People seeking mental-health support</option>
          </select>
        </div>

        <div>
          <label for="c">Geographic context</label>
          <select id="c" bind:value={context}>
            <option>India</option>
            <option>Goa, India</option>
            <option>General / international</option>
          </select>
        </div>
      </div>

      <label>Sample questions</label>

      {#each examples as ex}
        <button
          type="button"
          class="sample"
          onclick={() => (question = ex)}
        >
          {ex}
        </button>
      {/each}

      <button
        type="button"
        class="primary"
        onclick={analyse}
        disabled={loading}
      >
        {loading ? 'Analysing evidence…' : 'Generate policy analysis →'}
      </button>

      {#if error}
        <div class="error">
          <b>Analysis failed</b>
          <p>{error}</p>
          <small>
            Check backend terminal, GROQ_API_KEY and dependencies.
          </small>
        </div>
      {/if}
    </section>

    <aside>
      <section class="panel">
        <div class="eyebrow">02 / AGENT WORKFLOW</div>
        <h2>How the agent works</h2>

        <ol>
          <li>
            <b>Interpret</b><br />
            <span>Identify population and policy objective.</span>
          </li>
          <li>
            <b>Retrieve</b><br />
            <span>Call the MCP evidence-search tool.</span>
          </li>
          <li>
            <b>Analyse</b><br />
            <span>Apply the policy-analysis skill.</span>
          </li>
          <li>
            <b>Report</b><br />
            <span>Explain evidence, feasibility and trade-offs.</span>
          </li>
        </ol>
      </section>

      <section class="notice">
        <b>Responsible use</b>
        <p>
          This prototype supports policy scoping, not diagnosis or treatment.
          Mindfulness does not replace professional care or improvements to
          harmful learning and working conditions.
        </p>
      </section>
    </aside>
  </main>

  {#if result}
    <section class="panel output">
      <div class="eyebrow">GENERATED POLICY BRIEF</div>
      <h2>Analysis and recommendation</h2>

      <div class="pills">
        <span>Model: {result.model}</span>
        <span>LangChain create_agent</span>
        <span class:good={result.tool_used}>
          {result.tool_used
            ? 'MCP tool called'
            : 'Tool call not confirmed'}
        </span>
      </div>

      <article class="markdown-output">
        {@html renderedAnswer}
      </article>

      <h3>Evidence sources</h3>
      <ul>
        {#each result.evidence_sources || [] as s}
          <li>
            <a
              href={s.slice(s.indexOf('https://'))}
              target="_blank"
              rel="noreferrer"
            >
              {s}
            </a>
          </li>
        {/each}
      </ul>

      <h3>Limitations</h3>
      <ul>
        {#each result.limitations || [] as x}
          <li>{x}</li>
        {/each}
      </ul>
    </section>
  {/if}

  <footer>
    <span>MindWell Policy Advisor · Exam prototype</span>
    <span>LLM-assisted · evidence-aware · human-reviewed</span>
  </footer>
</div>

<style>
  :global(*) {
    box-sizing: border-box;
  }

  :global(body) {
    margin: 0;
    background: #f2f6f7;
    color: #18303a;
    font-family: Inter, system-ui, sans-serif;
  }

  .page {
    max-width: 1150px;
    margin: auto;
    padding: 38px 24px;
  }

  .eyebrow {
    font-size: 0.72rem;
    letter-spacing: 0.13em;
    font-weight: 800;
    color: #087e83;
  }

  h1 {
    font-size: clamp(2rem, 5vw, 3.4rem);
    letter-spacing: -0.05em;
    margin: 12px 0;
  }

  h1 span {
    color: #07858a;
  }

  .sub,
  .muted {
    color: #71818a;
    line-height: 1.55;
  }

  .sub {
    max-width: 720px;
    margin-bottom: 28px;
  }

  main {
    display: grid;
    grid-template-columns: 1.4fr 0.8fr;
    gap: 18px;
    align-items: start;
  }

  .panel {
    background: white;
    border: 1px solid #e0e8eb;
    border-radius: 17px;
    padding: 24px;
    box-shadow: 0 8px 28px #1b354108;
  }

  h2 {
    font-size: 1.2rem;
    margin: 9px 0;
  }

  label {
    display: block;
    font-size: 0.82rem;
    font-weight: 750;
    margin: 15px 0 7px;
  }

  textarea,
  select {
    width: 100%;
    border: 1px solid #d4e0e3;
    border-radius: 9px;
    padding: 12px;
    font: inherit;
    background: #fbfcfd;
    color: #213740;
  }

  .twocol {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .sample {
    display: block;
    text-align: left;
    width: 100%;
    padding: 9px 11px;
    margin: 7px 0;
    border: 1px solid #e0e8eb;
    background: #f7f9fa;
    border-radius: 8px;
    color: #455b64;
    cursor: pointer;
  }

  .sample:hover {
    background: #eaf4f4;
    border-color: #b9d9da;
  }

  .primary {
    width: 100%;
    margin-top: 16px;
    background: #087f83;
    color: white;
    padding: 14px;
    border: 0;
    border-radius: 9px;
    font-weight: 800;
    cursor: pointer;
  }

  .primary:disabled {
    opacity: 0.65;
    cursor: wait;
  }

  aside {
    display: grid;
    gap: 15px;
  }

  ol {
    padding-left: 21px;
    line-height: 1.5;
  }

  ol li {
    margin: 15px 0;
  }

  ol span {
    color: #6a7b84;
    font-size: 0.9rem;
  }

  .notice {
    background: #e3f4f1;
    border: 1px solid #cfe9e5;
    padding: 18px;
    border-radius: 13px;
    color: #176c6d;
  }

  .notice p {
    font-size: 0.88rem;
    line-height: 1.55;
    margin-bottom: 0;
    color: #45666a;
  }

  .error {
    background: #fff0ef;
    color: #8c3029;
    border-radius: 9px;
    padding: 12px;
    margin-top: 12px;
    overflow-wrap: anywhere;
  }

  .output {
    margin-top: 20px;
  }

  .pills {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin: 15px 0;
  }

  .pills span {
    font-size: 0.75rem;
    padding: 6px 9px;
    border-radius: 7px;
    background: #edf2f3;
    color: #50656e;
  }

  .pills .good {
    background: #ddf5e9;
    color: #176742;
  }

  /* Markdown output styling */
  .markdown-output {
    line-height: 1.65;
    overflow-wrap: anywhere;
    color: #293e48;
  }

  .markdown-output h1,
  .markdown-output h2,
  .markdown-output h3 {
    margin-top: 1.25rem;
    margin-bottom: 0.6rem;
  }

  .markdown-output p {
    margin: 0.7rem 0;
  }

  .markdown-output ul,
  .markdown-output ol {
    padding-left: 1.5rem;
    margin: 0.7rem 0;
  }

  .markdown-output table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    display: block;
    overflow-x: auto;
  }

  .markdown-output th,
  .markdown-output td {
    border: 1px solid #d7dee5;
    padding: 0.65rem;
    text-align: left;
    vertical-align: top;
  }

  .markdown-output th {
    background: #f0f4f8;
    font-weight: 600;
  }

  .markdown-output a {
    text-decoration: underline;
    overflow-wrap: anywhere;
  }

  .markdown-output code {
    background: #f1f3f5;
    padding: 0.15rem 0.3rem;
    border-radius: 4px;
  }

  .markdown-output pre {
    overflow-x: auto;
    padding: 0.8rem;
    border-radius: 6px;
    background: #f1f3f5;
  }

  h3 {
    margin-top: 25px;
    font-size: 1rem;
  }

  li {
    line-height: 1.55;
    color: #52666f;
    font-size: 0.9rem;
  }

  a {
    color: #087b80;
    overflow-wrap: anywhere;
  }

  footer {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    color: #84929a;
    font-size: 0.76rem;
    margin-top: 25px;
  }

  @media (max-width: 780px) {
    .page {
      padding: 24px 14px;
    }

    main,
    .twocol {
      grid-template-columns: 1fr;
    }

    .panel {
      padding: 18px;
    }

    footer {
      flex-direction: column;
    }
  }
</style>
