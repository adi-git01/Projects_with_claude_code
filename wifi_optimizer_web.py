#!/usr/bin/env python3
"""
WiFi Optimizer - Web GUI

A simple web interface for optimizing your home WiFi network.
Run this script and open http://localhost:5000 in your browser.
"""

import json
import sys
import os
from flask import Flask, render_template_string, jsonify, request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wifi_optimizer.models.network import NetworkDevice, Location, DeviceType
from wifi_optimizer.models.config import NetworkConfig
from wifi_optimizer.scanners.wifi_scanner import get_scanner
from wifi_optimizer.analyzers.channel_analyzer import ChannelAnalyzer
from wifi_optimizer.analyzers.placement_advisor import PlacementAdvisor
from wifi_optimizer.collectors.measurement_collector import MeasurementCollector

app = Flask(__name__)

# Global state
config = NetworkConfig()
scanner = get_scanner()
collector = MeasurementCollector(scanner)
channel_analyzer = ChannelAnalyzer()


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WiFi Optimizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: #fff;
            padding: 20px;
        }

        .container {
            max-width: 1000px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            padding: 30px 0;
        }

        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #4ecca3, #e94560);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        header p {
            color: #a0a0a0;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: rgba(22, 33, 62, 0.8);
            border-radius: 15px;
            padding: 25px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }

        .card h2 {
            font-size: 1.2em;
            margin-bottom: 15px;
            color: #4ecca3;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .card h2 .step {
            background: #4ecca3;
            color: #1a1a2e;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9em;
        }

        label {
            display: block;
            margin-bottom: 5px;
            color: #a0a0a0;
            font-size: 0.9em;
        }

        input, select {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            background: rgba(15, 52, 96, 0.8);
            color: #fff;
            margin-bottom: 15px;
            font-size: 1em;
        }

        input:focus, select:focus {
            outline: 2px solid #4ecca3;
        }

        button {
            width: 100%;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.3);
        }

        button:active {
            transform: translateY(0);
        }

        .btn-primary {
            background: linear-gradient(90deg, #4ecca3, #3db892);
            color: #1a1a2e;
        }

        .btn-secondary {
            background: rgba(15, 52, 96, 0.8);
            color: #fff;
            margin-bottom: 10px;
        }

        .btn-action {
            background: linear-gradient(90deg, #e94560, #d63550);
            color: #fff;
        }

        .location-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }

        .tag {
            background: rgba(15, 52, 96, 0.8);
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            cursor: pointer;
            transition: background 0.2s;
        }

        .tag:hover {
            background: #4ecca3;
            color: #1a1a2e;
        }

        .tag.selected {
            background: #4ecca3;
            color: #1a1a2e;
        }

        .results-card {
            grid-column: 1 / -1;
        }

        #results {
            background: rgba(15, 52, 96, 0.5);
            border-radius: 10px;
            padding: 20px;
            font-family: 'Consolas', monospace;
            white-space: pre-wrap;
            max-height: 500px;
            overflow-y: auto;
            line-height: 1.6;
        }

        .network-item {
            background: rgba(15, 52, 96, 0.5);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 10px;
        }

        .network-item.your-network {
            border-left: 3px solid #4ecca3;
        }

        .signal-bar {
            height: 8px;
            background: rgba(255,255,255,0.1);
            border-radius: 4px;
            margin-top: 8px;
            overflow: hidden;
        }

        .signal-bar-fill {
            height: 100%;
            border-radius: 4px;
            transition: width 0.3s;
        }

        .signal-excellent { background: #4ecca3; }
        .signal-good { background: #7ed957; }
        .signal-fair { background: #ffc107; }
        .signal-weak { background: #ff6b6b; }

        .recommendation-box {
            background: rgba(78, 204, 163, 0.1);
            border: 1px solid #4ecca3;
            border-radius: 10px;
            padding: 20px;
            margin-top: 15px;
        }

        .recommendation-box h3 {
            color: #4ecca3;
            margin-bottom: 15px;
        }

        .rec-item {
            margin-bottom: 10px;
            padding-left: 20px;
            position: relative;
        }

        .rec-item::before {
            content: "→";
            position: absolute;
            left: 0;
            color: #4ecca3;
        }

        .loading {
            text-align: center;
            padding: 20px;
            color: #a0a0a0;
        }

        .loading::after {
            content: "";
            animation: dots 1.5s infinite;
        }

        @keyframes dots {
            0%, 20% { content: "."; }
            40% { content: ".."; }
            60%, 100% { content: "..."; }
        }

        .status {
            text-align: center;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 8px;
            display: none;
        }

        .status.show {
            display: block;
        }

        .status.success {
            background: rgba(78, 204, 163, 0.2);
            color: #4ecca3;
        }

        .status.error {
            background: rgba(233, 69, 96, 0.2);
            color: #e94560;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>WiFi Optimizer</h1>
            <p>Optimize your Airtel + Tenda repeater setup</p>
        </header>

        <div id="status" class="status"></div>

        <div class="cards">
            <!-- Device Setup -->
            <div class="card">
                <h2><span class="step">1</span> Your Devices</h2>

                <label>Main Router SSID (Airtel)</label>
                <input type="text" id="router-ssid" placeholder="e.g., Airtel_Home" value="Airtel_Home">

                <label>Number of Repeaters (Tenda)</label>
                <select id="repeater-count">
                    <option value="1">1 Repeater</option>
                    <option value="2" selected>2 Repeaters</option>
                    <option value="3">3 Repeaters</option>
                </select>

                <button class="btn-primary" onclick="saveDevices()">Save Devices</button>
            </div>

            <!-- Locations -->
            <div class="card">
                <h2><span class="step">2</span> Locations</h2>

                <label>Quick Add (click to add)</label>
                <div class="location-tags" id="quick-locations">
                    <span class="tag" onclick="addLocation('Living Room')">Living Room</span>
                    <span class="tag" onclick="addLocation('Bedroom')">Bedroom</span>
                    <span class="tag" onclick="addLocation('Kitchen')">Kitchen</span>
                    <span class="tag" onclick="addLocation('Study')">Study</span>
                    <span class="tag" onclick="addLocation('Balcony')">Balcony</span>
                </div>

                <label>Your Locations</label>
                <div class="location-tags" id="selected-locations"></div>

                <input type="text" id="custom-location" placeholder="Add custom location..." onkeypress="if(event.key==='Enter')addCustomLocation()">
            </div>

            <!-- Actions -->
            <div class="card">
                <h2><span class="step">3</span> Actions</h2>

                <button class="btn-secondary" onclick="scanNetworks()">
                    Scan WiFi Networks
                </button>

                <button class="btn-secondary" onclick="measureLocation()">
                    Measure Current Location
                </button>

                <button class="btn-action" onclick="getRecommendations()">
                    Get Recommendations
                </button>
            </div>

            <!-- Results -->
            <div class="card results-card">
                <h2>Results</h2>
                <div id="results">
Welcome to WiFi Optimizer!

Steps:
1. Enter your router SSID and save
2. Add locations where you use WiFi
3. Click "Scan WiFi Networks"
4. Click "Get Recommendations" for optimization tips

For best results:
- Move your laptop to each location
- Click "Measure Current Location" at each spot
- Then get personalized placement recommendations
                </div>
            </div>
        </div>
    </div>

    <script>
        let selectedLocations = [];
        let currentLocationIndex = 0;

        function showStatus(message, type) {
            const status = document.getElementById('status');
            status.textContent = message;
            status.className = 'status show ' + type;
            setTimeout(() => status.className = 'status', 3000);
        }

        function saveDevices() {
            const ssid = document.getElementById('router-ssid').value;
            const count = document.getElementById('repeater-count').value;

            fetch('/api/save-devices', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ssid: ssid, repeater_count: parseInt(count)})
            })
            .then(r => r.json())
            .then(data => {
                showStatus('Devices saved!', 'success');
            });
        }

        function addLocation(name) {
            if (!selectedLocations.includes(name)) {
                selectedLocations.push(name);
                updateLocationTags();

                fetch('/api/add-location', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name: name})
                });
            }
        }

        function addCustomLocation() {
            const input = document.getElementById('custom-location');
            const name = input.value.trim();
            if (name) {
                addLocation(name);
                input.value = '';
            }
        }

        function updateLocationTags() {
            const container = document.getElementById('selected-locations');
            container.innerHTML = selectedLocations.map(loc =>
                `<span class="tag selected">${loc}</span>`
            ).join('');
        }

        function scanNetworks() {
            document.getElementById('results').innerHTML = '<div class="loading">Scanning networks</div>';

            fetch('/api/scan')
            .then(r => r.json())
            .then(data => {
                displayNetworks(data.networks);
                showStatus(`Found ${data.networks.length} networks`, 'success');
            });
        }

        function displayNetworks(networks) {
            const ssid = document.getElementById('router-ssid').value;
            let html = '<h3 style="margin-bottom:15px">Networks Found</h3>';

            networks.sort((a, b) => b.signal_dbm - a.signal_dbm);

            networks.forEach(net => {
                const isYours = net.ssid === ssid;
                const pct = Math.min(100, Math.max(0, 2 * (net.signal_dbm + 100)));
                let colorClass = 'signal-weak';
                if (pct >= 80) colorClass = 'signal-excellent';
                else if (pct >= 60) colorClass = 'signal-good';
                else if (pct >= 40) colorClass = 'signal-fair';

                html += `
                    <div class="network-item ${isYours ? 'your-network' : ''}">
                        <strong>${net.ssid}</strong> ${isYours ? '⭐' : ''}
                        <span style="float:right;color:#a0a0a0">
                            Ch ${net.channel} | ${net.signal_dbm} dBm | ${net.quality}
                        </span>
                        <div class="signal-bar">
                            <div class="signal-bar-fill ${colorClass}" style="width:${pct}%"></div>
                        </div>
                    </div>
                `;
            });

            document.getElementById('results').innerHTML = html;
        }

        function measureLocation() {
            if (selectedLocations.length === 0) {
                showStatus('Please add locations first', 'error');
                return;
            }

            const loc = selectedLocations[currentLocationIndex];
            currentLocationIndex = (currentLocationIndex + 1) % selectedLocations.length;

            document.getElementById('results').innerHTML = `<div class="loading">Measuring at ${loc}</div>`;

            fetch('/api/measure', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({location: loc})
            })
            .then(r => r.json())
            .then(data => {
                displayMeasurements(data.coverage);
                showStatus(`Measured at ${loc}`, 'success');
            });
        }

        function displayMeasurements(coverage) {
            let html = '<h3 style="margin-bottom:15px">Signal Measurements</h3>';

            for (const [location, signals] of Object.entries(coverage)) {
                for (const [ssid, signal] of Object.entries(signals)) {
                    const pct = Math.min(100, Math.max(0, 2 * (signal + 100)));
                    let quality = 'Dead Zone';
                    let colorClass = 'signal-weak';
                    if (signal >= -50) { quality = 'Excellent'; colorClass = 'signal-excellent'; }
                    else if (signal >= -60) { quality = 'Good'; colorClass = 'signal-good'; }
                    else if (signal >= -70) { quality = 'Fair'; colorClass = 'signal-fair'; }
                    else if (signal >= -80) { quality = 'Weak'; }

                    html += `
                        <div class="network-item">
                            <strong>${location}</strong>
                            <span style="float:right">${signal.toFixed(0)} dBm - ${quality}</span>
                            <div class="signal-bar">
                                <div class="signal-bar-fill ${colorClass}" style="width:${pct}%"></div>
                            </div>
                        </div>
                    `;
                }
            }

            html += `
                <div style="margin-top:20px;padding:15px;background:rgba(15,52,96,0.5);border-radius:8px">
                    <strong>Signal Guide:</strong><br>
                    > -50 dBm = Excellent<br>
                    -50 to -60 = Good<br>
                    -60 to -70 = Fair (ideal for repeater placement)<br>
                    -70 to -80 = Weak<br>
                    < -80 = Dead Zone
                </div>
            `;

            document.getElementById('results').innerHTML = html;
        }

        function getRecommendations() {
            document.getElementById('results').innerHTML = '<div class="loading">Analyzing</div>';

            fetch('/api/recommendations')
            .then(r => r.json())
            .then(data => {
                displayRecommendations(data);
                showStatus('Recommendations ready!', 'success');
            });
        }

        function displayRecommendations(data) {
            const ch = data.channels;
            const placements = data.placements;

            let html = `
                <div class="recommendation-box">
                    <h3>Router Settings (Airtel)</h3>
                    <div class="rec-item"><strong>2.4GHz Channel:</strong> ${ch['2.4GHz'].channel}</div>
                    <div class="rec-item"><strong>2.4GHz Width:</strong> 20 MHz</div>
                    <div class="rec-item"><strong>5GHz Channel:</strong> ${ch['5GHz'].channel}</div>
                    <div class="rec-item"><strong>5GHz Width:</strong> 40 MHz</div>
                </div>

                <div class="recommendation-box" style="margin-top:15px">
                    <h3>Repeater Settings (Tenda)</h3>
                    <div class="rec-item">Use <strong>same channels</strong> as router</div>
                    <div class="rec-item">Use <strong>same SSID</strong> and password</div>
                </div>

                <div class="recommendation-box" style="margin-top:15px">
                    <h3>Repeater Placement</h3>
            `;

            placements.forEach(p => {
                html += `
                    <div style="margin-bottom:15px;padding:10px;background:rgba(0,0,0,0.2);border-radius:8px">
                        <strong>${p.name}</strong><br>
                        <span style="color:#4ecca3">📍 ${p.location}</span><br>
                        <small style="color:#a0a0a0">${p.reasoning[0]}</small>
                    </div>
                `;
            });

            html += `
                </div>

                <div class="recommendation-box" style="margin-top:15px;border-color:#e94560">
                    <h3 style="color:#e94560">Action Steps</h3>
                    <div class="rec-item">Log into router at 192.168.1.1</div>
                    <div class="rec-item">Set channels as recommended above</div>
                    <div class="rec-item">Place repeaters at suggested locations</div>
                    <div class="rec-item">Configure repeaters with same SSID/password</div>
                    <div class="rec-item">Test coverage by walking around with phone!</div>
                </div>
            `;

            document.getElementById('results').innerHTML = html;
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/save-devices', methods=['POST'])
def save_devices():
    data = request.json
    ssid = data.get('ssid', 'WiFi')
    repeater_count = data.get('repeater_count', 2)

    # Clear and add devices
    config.devices = []

    main_router = NetworkDevice(
        name="Airtel Main Router",
        device_type=DeviceType.MAIN_ROUTER,
        ssid=ssid,
        ip_address="192.168.1.1"
    )
    config.add_device(main_router)

    for i in range(repeater_count):
        repeater = NetworkDevice(
            name=f"Tenda Repeater {i + 1}",
            device_type=DeviceType.REPEATER,
            ssid=ssid
        )
        config.add_device(repeater)

    collector.set_your_networks([ssid])
    channel_analyzer.set_your_ssids([ssid])

    return jsonify({'status': 'ok'})


@app.route('/api/add-location', methods=['POST'])
def add_location():
    data = request.json
    name = data.get('name', '')

    location = Location(name=name, priority=len(config.locations) + 1)
    config.add_location(location)

    return jsonify({'status': 'ok'})


@app.route('/api/scan')
def scan_networks():
    networks = scanner.scan()
    channel_analyzer.set_networks(networks)

    network_data = []
    for net in networks:
        network_data.append({
            'ssid': net.ssid,
            'bssid': net.bssid,
            'signal_dbm': net.signal_dbm,
            'channel': net.channel,
            'band': net.frequency_band.value,
            'quality': net.signal_quality
        })

    return jsonify({'networks': network_data})


@app.route('/api/measure', methods=['POST'])
def measure():
    data = request.json
    loc_name = data.get('location', 'Unknown')

    location = Location(name=loc_name, priority=1)
    collector.collect_at_location(location, num_samples=2)

    coverage = collector.get_your_networks_coverage()
    return jsonify({'coverage': coverage})


@app.route('/api/recommendations')
def recommendations():
    # Make sure we have network data
    networks = scanner.scan()
    channel_analyzer.set_networks(networks)

    # Get channel recommendations
    channel_recs = channel_analyzer.get_configuration_recommendations()

    # Get placement recommendations
    num_repeaters = len(config.get_repeaters()) or 2
    placement_advisor = PlacementAdvisor(collector)
    placement_advisor.set_devices(config.devices)
    placements = placement_advisor.get_placement_recommendations(num_repeaters)

    placement_data = []
    for p in placements:
        placement_data.append({
            'name': p.repeater_name,
            'location': p.recommended_location,
            'connect_to': p.should_connect_to,
            'reasoning': p.reasoning
        })

    return jsonify({
        'channels': channel_recs,
        'placements': placement_data
    })


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("  WiFi Optimizer Web GUI")
    print("=" * 50)
    print("\n  Open your browser to: http://localhost:5000")
    print("\n  Press Ctrl+C to stop the server")
    print("=" * 50 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=False)
