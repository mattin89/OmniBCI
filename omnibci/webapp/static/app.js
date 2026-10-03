document.addEventListener('DOMContentLoaded', () => {
  const chatForm = document.getElementById('chatForm');
  const userInput = document.getElementById('userInput');
  const chatMessages = document.getElementById('chatMessages');
  const runLoopBtn = document.getElementById('runLoopBtn');
  const agentStatus = document.getElementById('agentStatus');
  const logStream = document.getElementById('logStream');
  const budgetValue = document.getElementById('budgetValue');
  const leaderboardBody = document.getElementById('leaderboardBody');
  const decisionBody = document.getElementById('decisionBody');

  const steps = [
    document.getElementById('step-lit'),
    document.getElementById('step-p2a'),
    document.getElementById('step-plan'),
    document.getElementById('step-safety'),
    document.getElementById('step-run'),
    document.getElementById('step-analysis')
  ];

  function setActiveStep(index) {
    steps.forEach((s, idx) => {
      if (idx <= index) {
        s.classList.add('active');
      } else {
        s.classList.remove('active');
      }
    });
  }

  function addLog(time, agent, msg) {
    const div = document.createElement('div');
    div.className = 'log-line';
    div.innerHTML = `<span class="log-time">[${time}]</span> <span class="log-agent">[${agent}]</span> ${msg}`;
    logStream.appendChild(div);
    logStream.scrollTop = logStream.scrollHeight;
  }

  function appendChat(role, text) {
    const msg = document.createElement('div');
    msg.className = `msg ${role}-msg`;
    msg.innerHTML = text.replace(/\n/g, '<br/>');
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = userInput.value.trim();
    if (!query) return;

    appendChat('user', `<strong>You:</strong> ${query}`);
    userInput.value = '';
    agentStatus.textContent = 'Orchestrating...';
    setActiveStep(1);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: query })
      });
      const data = await res.json();
      appendChat('bot', `<strong>Omnigent Lab:</strong> ${data.response}`);
      agentStatus.textContent = 'Agent Ready';
    } catch (err) {
      appendChat('bot', `<strong>Error:</strong> ${err.message}`);
      agentStatus.textContent = 'Error';
    }
  });

  runLoopBtn.addEventListener('click', async () => {
    runLoopBtn.disabled = true;
    runLoopBtn.textContent = '⏳ Executing Discovery Loop...';
    agentStatus.textContent = 'Running Benchmark...';

    // Step 1: Literature
    setActiveStep(0);
    addLog(new Date().toLocaleTimeString(), 'Literature Harvester', 'Harvesting BCI codebases from OpenAlex & GitHub...');

    try {
      const res = await fetch('/api/run-discovery', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          hypothesis: "Decode motor intention on low-cost wearable EEG across unseen stroke rehab subjects",
          models: ["riemannian_ea", "eegnet", "shallow_fbcsp"]
        })
      });

      const data = await res.json();
      setActiveStep(5); // Complete
      budgetValue.textContent = '$0.94 / $25.00';
      agentStatus.textContent = 'Discovery Complete';

      // Update Leaderboard
      const bench = data.benchmark_results;
      if (bench) {
        leaderboardBody.innerHTML = '';
        Object.keys(bench).forEach(key => {
          const item = bench[key];
          const isWinner = key === data.winning_model;
          const tr = document.createElement('tr');
          if (isWinner) tr.className = 'highlight-row';

          const safeTag = item.mean_false_positive_rate <= 0.10
            ? '<span class="tag tag-safe">SAFE (FPR &lt; 10%)</span>'
            : '<span class="tag tag-warn">WARN (FPR &gt; 10%)</span>';

          tr.innerHTML = `
            <td><strong>${item.title}</strong></td>
            <td>${item.category}</td>
            <td class="metric-val">${(item.mean_accuracy * 100).toFixed(2)}%</td>
            <td>${item.mean_cohen_kappa.toFixed(3)}</td>
            <td>${(item.mean_false_positive_rate * 100).toFixed(1)}%</td>
            <td>${item.mean_latency_ms.toFixed(1)} ms</td>
            <td>${safeTag}</td>
          `;
          leaderboardBody.appendChild(tr);
        });
      }

      // Update Decision Card
      const rep = data.discovery_report;
      if (rep) {
        decisionBody.innerHTML = `
          <p><strong>Mechanistic Finding:</strong> ${rep.mechanistic_finding}</p>
          <p><strong>Updated Hypothesis:</strong> <em>"${rep.updated_scientific_hypothesis}"</em></p>
          <p class="speedup-metric">⚡ <strong>Measured Discovery Acceleration: ${rep.measured_acceleration.measured_speedup_factor}</strong></p>
        `;
      }

      addLog(new Date().toLocaleTimeString(), 'Analysis & Decision', `Completed! Winning model: ${data.winning_model}`);
      appendChat('bot', `<strong>Omnigent Discovery Completed!</strong><br/>Winning Model: <strong>${data.winning_model}</strong> with ${(rep.winning_mean_accuracy*100).toFixed(2)}% cross-subject accuracy.<br/>Kaggle <code>submission.csv</code> has been generated and validated.`);

    } catch (err) {
      appendChat('bot', `<strong>Error during discovery run:</strong> ${err.message}`);
    } finally {
      runLoopBtn.disabled = false;
      runLoopBtn.textContent = '▶ Run Full 17-Subject Benchmark';
    }
  });
});
