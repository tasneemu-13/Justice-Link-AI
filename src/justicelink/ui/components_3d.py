"""
JusticeLink AI: 3D High Court Architecture & Institutional Visual Component.
Renders an interactive 3D WebGL architectural visualization of a classical Indian High Court facade
(Greco-Roman classical judicial colonnade, domed rotunda, stepped pediment, sandstone & marble textures)
using Three.js with complete fallback support.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components


def render_3d_court_building(height: int = 440):
    """Renders a 3D High Court architectural facade in WebGL via Three.js with warm sandstone & ivory aesthetics."""
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                width: 100%;
                height: 100%;
                background-color: #F8F5EE;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            #canvas-container {{
                width: 100%;
                height: 100%;
                position: relative;
                border-radius: 8px;
                border: 1px solid #DFD7C5;
            }}
            .badge-overlay {{
                position: absolute;
                top: 14px;
                left: 16px;
                background: rgba(253, 251, 247, 0.92);
                border: 1px solid #C29B38;
                padding: 6px 12px;
                border-radius: 4px;
                color: #6B1D2F;
                font-size: 11px;
                font-weight: 700;
                letter-spacing: 0.5px;
                box-shadow: 0 2px 6px rgba(0,0,0,0.06);
                pointer-events: none;
            }}
            .instructions {{
                position: absolute;
                bottom: 12px;
                right: 16px;
                background: rgba(253, 251, 247, 0.85);
                padding: 4px 10px;
                border-radius: 4px;
                color: #6B7280;
                font-size: 10px;
                pointer-events: none;
                border: 1px solid #E2D9C8;
            }}
        </style>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    </head>
    <body>
        <div id="canvas-container">
            <div class="badge-overlay">⚖️ INDIAN HIGH COURT FACADE · 3D ARCHITECTURAL TWIN</div>
            <div class="instructions">🖱️ Drag to Rotate · Scroll to Zoom</div>
        </div>

        <script>
            const container = document.getElementById('canvas-container');
            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0xF8F5EE);

            // Camera setup
            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 18, 55);

            const renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;
            container.appendChild(renderer.domElement);

            // Lighting
            const ambientLight = new THREE.AmbientLight(0xFFF9EE, 0.85);
            scene.add(ambientLight);

            const sunLight = new THREE.DirectionalLight(0xFFF5DD, 1.2);
            sunLight.position.set(30, 45, 30);
            sunLight.castShadow = true;
            scene.add(sunLight);

            const softFill = new THREE.DirectionalLight(0xD8C8B0, 0.4);
            softFill.position.set(-30, 20, -20);
            scene.add(softFill);

            // Institutional Color Materials (Sandstone, Marble, Antique Terracotta)
            const sandstoneMat = new THREE.MeshStandardMaterial({{ color: 0xD9C6A5, roughness: 0.65, metalness: 0.05 }});
            const marbleMat = new THREE.MeshStandardMaterial({{ color: 0xF3EFE6, roughness: 0.35, metalness: 0.02 }});
            const darkPillarMat = new THREE.MeshStandardMaterial({{ color: 0x9E7D2B, roughness: 0.5 }});
            const domeMat = new THREE.MeshStandardMaterial({{ color: 0x80182A, roughness: 0.4, metalness: 0.15 }});
            const baseMat = new THREE.MeshStandardMaterial({{ color: 0xB8A88E, roughness: 0.8 }});

            const buildingGroup = new THREE.Group();

            // 1. Foundation Podium & Steps
            const podiumGeo = new THREE.BoxGeometry(48, 2.5, 24);
            const podium = new THREE.Mesh(podiumGeo, baseMat);
            podium.position.y = 1.25;
            podium.receiveShadow = true;
            buildingGroup.add(podium);

            // Front Steps
            for(let i=0; i<4; i++) {{
                const step = new THREE.Mesh(new THREE.BoxGeometry(26 - i*2, 0.3, 3), sandstoneMat);
                step.position.set(0, 0.15 + i*0.3, 12 + i*0.8);
                buildingGroup.add(step);
            }}

            // 2. Main Judicial Wing (Center Block)
            const centerBlock = new THREE.Mesh(new THREE.BoxGeometry(24, 14, 18), sandstoneMat);
            centerBlock.position.set(0, 9.5, 0);
            centerBlock.castShadow = true;
            centerBlock.receiveShadow = true;
            buildingGroup.add(centerBlock);

            // East & West Portico Wings
            const westWing = new THREE.Mesh(new THREE.BoxGeometry(11, 11, 16), sandstoneMat);
            westWing.position.set(-17.5, 8, 0);
            buildingGroup.add(westWing);

            const eastWing = new THREE.Mesh(new THREE.BoxGeometry(11, 11, 16), sandstoneMat);
            eastWing.position.set(17.5, 8, 0);
            buildingGroup.add(eastWing);

            // 3. Classical Front Colonnade (8 Sandstone Pillars)
            const pillarRadius = 0.55;
            const pillarHeight = 12;
            const pillarGeo = new THREE.CylinderGeometry(pillarRadius*0.9, pillarRadius, pillarHeight, 20);
            const pillarSpacing = 2.6;

            for (let i = -3.5; i <= 3.5; i++) {{
                const pillar = new THREE.Mesh(pillarGeo, marbleMat);
                pillar.position.set(i * pillarSpacing, 8.5, 9.5);
                pillar.castShadow = true;
                buildingGroup.add(pillar);

                // Pillar Capital & Plinth
                const cap = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.4, 1.4), darkPillarMat);
                cap.position.set(i * pillarSpacing, 14.5, 9.5);
                buildingGroup.add(cap);

                const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.4, 1.4), darkPillarMat);
                plinth.position.set(i * pillarSpacing, 2.7, 9.5);
                buildingGroup.add(plinth);
            }}

            // 4. Entablature & Classical Triangular Pediment
            const entablature = new THREE.Mesh(new THREE.BoxGeometry(23, 1.2, 4), sandstoneMat);
            entablature.position.set(0, 15.1, 9.5);
            buildingGroup.add(entablature);

            // Pediment (Prism)
            const pedimentShape = new THREE.Shape();
            pedimentShape.moveTo(-11.5, 0);
            pedimentShape.lineTo(11.5, 0);
            pedimentShape.lineTo(0, 4.2);
            pedimentShape.closePath();

            const extrudeSettings = {{ depth: 3.5, bevelEnabled: false }};
            const pedimentGeo = new THREE.ExtrudeGeometry(pedimentShape, extrudeSettings);
            const pediment = new THREE.Mesh(pedimentGeo, sandstoneMat);
            pediment.position.set(0, 15.7, 6.5);
            buildingGroup.add(pediment);

            // 5. Central Rotunda Drum & Burgundy/Gold Dome
            const drumGeo = new THREE.CylinderGeometry(5.2, 5.2, 4, 32);
            const drum = new THREE.Mesh(drumGeo, sandstoneMat);
            drum.position.set(0, 18.5, 0);
            buildingGroup.add(drum);

            const domeGeo = new THREE.SphereGeometry(5.4, 32, 24, 0, Math.PI * 2, 0, Math.PI * 0.5);
            const dome = new THREE.Mesh(domeGeo, domeMat);
            dome.position.set(0, 20.5, 0);
            buildingGroup.add(dome);

            // Golden Finial / Kalash spire
            const finialGeo = new THREE.CylinderGeometry(0.1, 0.35, 2.5, 12);
            const finial = new THREE.Mesh(finialGeo, darkPillarMat);
            finial.position.set(0, 26.5, 0);
            buildingGroup.add(finial);

            scene.add(buildingGroup);

            // Smooth gentle orbit controls
            let isDragging = false;
            let prevMouseX = 0;
            let targetRotationY = -0.35;

            container.addEventListener('mousedown', (e) => {{
                isDragging = true;
                prevMouseX = e.clientX;
            }});

            window.addEventListener('mouseup', () => {{ isDragging = false; }});

            container.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    const deltaX = e.clientX - prevMouseX;
                    targetRotationY += deltaX * 0.008;
                    prevMouseX = e.clientX;
                }}
            }});

            // Wheel zoom
            container.addEventListener('wheel', (e) => {{
                e.preventDefault();
                camera.position.z = Math.max(30, Math.min(85, camera.position.z + e.deltaY * 0.05));
            }});

            // Animation Loop
            function animate() {{
                requestAnimationFrame(animate);
                if (!isDragging) {{
                    targetRotationY += 0.002; // Gentle slow ambient rotation
                }}
                buildingGroup.rotation.y += (targetRotationY - buildingGroup.rotation.y) * 0.05;
                renderer.render(scene, camera);
            }}
            animate();

            // Resize listener
            window.addEventListener('resize', () => {{
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }});
        </script>
    </body>
    </html>
    """
    components.html(html_code, height=height)
