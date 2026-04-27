<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Jus Cogens Core - Peremptory Norms</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f4f4f4; }
    header { background: #007BFF; color: white; text-align: center; padding: 2rem; }
    .container { max-width: 800px; margin: 0 auto; padding: 2rem; }
    .jus-cogens { background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); margin: 2rem 0; }
    .interactive { text-align: center; margin: 2rem 0; }
    button { background: #28a745; color: white; border: none; padding: 1rem; font-size: 1.2rem; cursor: pointer; border-radius: 5px; transition: background 0.3s; }
    button:hover { background: #218838; }
    #time-display { font-size: 2rem; margin: 1rem; color: #007BFF; }
    a { color: #007BFF; text-decoration: none; }
    a:hover { text-decoration: underline; }
  </style>
</head>
<body>
  <header><h1>Jus Cogens Core: Peremptory Norms for World Peace</h1><p>Interactive Norm of International Law</p></header>
  <div class="container">
    <div class="jus-cogens">
      <h2>What is Jus Cogens?</h2>
      <p>Peremptory norms of general international law (jus cogens) are fundamental norms from which no derogation is permitted. They are recognized by the international community as a whole and can only be modified by subsequent norms of the same character.</p>
      <h3>Article 53: Void Treaties</h3>
      <p>"A treaty is void if, at the time of its conclusion, it conflicts with a peremptory norm of general international law."</p>
      <h3>Article 64: Emergence of New Norms</h3>
      <p>"If a new peremptory norm of general international law emerges, any existing treaty which is in conflict with that norm becomes void and terminates."</p>
      <h2>Why Jus Cogens Ensures Peace</h2>
      <p>Jus cogens protects essential human rights such as the prohibition of torture, genocide, slavery, and other atrocities. By binding all states without exception, it creates a foundation for global justice and prevents wars rooted in violations of these norms.</p>
      <h2>Interactive Impact Over Time</h2>
      <div class="interactive">
        <button id="activate">Activate Jus Cogens Impact</button>
        <div id="time-display">Time since Vienna Convention: <span id="years">55</span> years</div>
        <div id="impact">Jus cogens has enforced <span id="violations">0</span> norms, preventing <span id="wars">0</span> conflicts.</div>
      </div>
      <p><a href="index.html">Back to Main Site</a></p>
    </div>
  </div>
  <script>
    let years = 55; // 2026 - 1969
    let violations = 0;
    let wars = 0;
    setInterval(() => {
      years += 0.01;
      document.getElementById('years').textContent = years.toFixed(2);
    }, 100);
    document.getElementById('activate').onclick = function() {
      violations += 10;
      wars += 1;
      document.getElementById('violations').textContent = violations;
      document.getElementById('wars').textContent = wars;
      alert('Jus cogens activated against a violation, enforcing peace!');
    };
  </script>
</body>
</html></content>
<parameter name="filePath">/mnt/c/Users/arhiv/apostille-legal-case/jus-cogens.html