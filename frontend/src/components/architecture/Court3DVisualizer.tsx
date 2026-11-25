import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

interface Court3DVisualizerProps {
  className?: string;
}

export const Court3DVisualizer: React.FC<Court3DVisualizerProps> = ({ className = 'h-[460px]' }) => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Scene
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0xF8F5EE);

    // Camera
    const camera = new THREE.PerspectiveCamera(
      45,
      container.clientWidth / container.clientHeight,
      0.1,
      1000
    );
    camera.position.set(0, 18, 55);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    container.appendChild(renderer.domElement);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xFFF9EE, 0.85);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xFFF5DD, 1.25);
    sunLight.position.set(30, 45, 30);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0xD8C8B0, 0.45);
    fillLight.position.set(-30, 20, -20);
    scene.add(fillLight);

    // Institutional Materials
    const sandstoneMat = new THREE.MeshStandardMaterial({ color: 0xD9C6A5, roughness: 0.65, metalness: 0.05 });
    const marbleMat = new THREE.MeshStandardMaterial({ color: 0xF3EFE6, roughness: 0.35, metalness: 0.02 });
    const goldMat = new THREE.MeshStandardMaterial({ color: 0x9E7D2B, roughness: 0.45, metalness: 0.25 });
    const domeMat = new THREE.MeshStandardMaterial({ color: 0x6B1D2F, roughness: 0.4, metalness: 0.15 });
    const baseMat = new THREE.MeshStandardMaterial({ color: 0xB8A88E, roughness: 0.8 });

    const buildingGroup = new THREE.Group();

    // 1. Podium Foundation & Steps
    const podium = new THREE.Mesh(new THREE.BoxGeometry(48, 2.5, 24), baseMat);
    podium.position.y = 1.25;
    podium.receiveShadow = true;
    buildingGroup.add(podium);

    for (let i = 0; i < 4; i++) {
      const step = new THREE.Mesh(new THREE.BoxGeometry(26 - i * 2, 0.3, 3), sandstoneMat);
      step.position.set(0, 0.15 + i * 0.3, 12 + i * 0.8);
      step.receiveShadow = true;
      buildingGroup.add(step);
    }

    // 2. Central Judicial Wing
    const centerBlock = new THREE.Mesh(new THREE.BoxGeometry(24, 14, 18), sandstoneMat);
    centerBlock.position.set(0, 9.5, 0);
    centerBlock.castShadow = true;
    centerBlock.receiveShadow = true;
    buildingGroup.add(centerBlock);

    // Wings
    const westWing = new THREE.Mesh(new THREE.BoxGeometry(11, 11, 16), sandstoneMat);
    westWing.position.set(-17.5, 8, 0);
    westWing.castShadow = true;
    buildingGroup.add(westWing);

    const eastWing = new THREE.Mesh(new THREE.BoxGeometry(11, 11, 16), sandstoneMat);
    eastWing.position.set(17.5, 8, 0);
    eastWing.castShadow = true;
    buildingGroup.add(eastWing);

    // 3. Colonnade (8 classical Pillars)
    const pillarRadius = 0.55;
    const pillarHeight = 12;
    const pillarGeo = new THREE.CylinderGeometry(pillarRadius * 0.9, pillarRadius, pillarHeight, 20);
    const pillarSpacing = 2.6;

    for (let i = -3.5; i <= 3.5; i++) {
      const pillar = new THREE.Mesh(pillarGeo, marbleMat);
      pillar.position.set(i * pillarSpacing, 8.5, 9.5);
      pillar.castShadow = true;
      buildingGroup.add(pillar);

      const cap = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.4, 1.4), goldMat);
      cap.position.set(i * pillarSpacing, 14.5, 9.5);
      buildingGroup.add(cap);

      const plinth = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.4, 1.4), goldMat);
      plinth.position.set(i * pillarSpacing, 2.7, 9.5);
      buildingGroup.add(plinth);
    }

    // 4. Classical Pediment
    const entablature = new THREE.Mesh(new THREE.BoxGeometry(23, 1.2, 4), sandstoneMat);
    entablature.position.set(0, 15.1, 9.5);
    buildingGroup.add(entablature);

    const pedimentShape = new THREE.Shape();
    pedimentShape.moveTo(-11.5, 0);
    pedimentShape.lineTo(11.5, 0);
    pedimentShape.lineTo(0, 4.2);
    pedimentShape.closePath();

    const pedimentGeo = new THREE.ExtrudeGeometry(pedimentShape, { depth: 3.5, bevelEnabled: false });
    const pediment = new THREE.Mesh(pedimentGeo, sandstoneMat);
    pediment.position.set(0, 15.7, 6.5);
    pediment.castShadow = true;
    buildingGroup.add(pediment);

    // 5. Central Rotunda Drum & Burgundy/Gold Dome
    const drum = new THREE.Mesh(new THREE.CylinderGeometry(5.2, 5.2, 4, 32), sandstoneMat);
    drum.position.set(0, 18.5, 0);
    buildingGroup.add(drum);

    const dome = new THREE.Mesh(
      new THREE.SphereGeometry(5.4, 32, 24, 0, Math.PI * 2, 0, Math.PI * 0.5),
      domeMat
    );
    dome.position.set(0, 20.5, 0);
    dome.castShadow = true;
    buildingGroup.add(dome);

    const finial = new THREE.Mesh(new THREE.CylinderGeometry(0.1, 0.35, 2.5, 12), goldMat);
    finial.position.set(0, 26.5, 0);
    buildingGroup.add(finial);

    scene.add(buildingGroup);

    // Interaction controls
    let isDragging = false;
    let prevMouseX = 0;
    let targetRotationY = -0.35;

    const onMouseDown = (e: MouseEvent) => {
      isDragging = true;
      prevMouseX = e.clientX;
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    const onMouseMove = (e: MouseEvent) => {
      if (isDragging) {
        const deltaX = e.clientX - prevMouseX;
        targetRotationY += deltaX * 0.008;
        prevMouseX = e.clientX;
      }
    };

    const onWheel = (e: WheelEvent) => {
      e.preventDefault();
      camera.position.z = Math.max(30, Math.min(85, camera.position.z + e.deltaY * 0.05));
    };

    container.addEventListener('mousedown', onMouseDown);
    window.addEventListener('mouseup', onMouseUp);
    container.addEventListener('mousemove', onMouseMove);
    container.addEventListener('wheel', onWheel, { passive: false });

    // Animation loop
    let animationFrameId: number;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (!isDragging) {
        targetRotationY += 0.0018; // Slow ambient orbit
      }
      buildingGroup.rotation.y += (targetRotationY - buildingGroup.rotation.y) * 0.05;
      renderer.render(scene, camera);
    };
    animate();

    const handleResize = () => {
      if (!container) return;
      camera.aspect = container.clientWidth / container.clientHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(container.clientWidth, container.clientHeight);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('mousedown', onMouseDown);
      window.removeEventListener('mouseup', onMouseUp);
      container.removeEventListener('mousemove', onMouseMove);
      container.removeEventListener('wheel', onWheel);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  return (
    <div className={`relative w-full rounded-xl overflow-hidden border border-[#DFD7C5] shadow-xs bg-[#F8F5EE] ${className}`}>
      <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />
      <div className="absolute top-4 left-4 pointer-events-none bg-[#FDFBF7]/90 backdrop-blur-xs border border-[#C29B38] px-3 py-1.5 rounded-sm shadow-xs flex items-center space-x-2">
        <span className="text-[#6B1D2F] font-serif text-xs font-bold tracking-wide">
          🏛️ INDIAN HIGH COURT FAÇADE
        </span>
        <span className="text-[10px] bg-[#EFE9DC] text-[#718096] px-1.5 py-0.5 rounded border border-[#DFD7C5]">
          3D Architectural Twin
        </span>
      </div>
      <div className="absolute bottom-3 right-4 pointer-events-none text-[11px] text-[#718096] bg-[#FDFBF7]/80 px-2 py-1 rounded border border-[#DFD7C5]/60">
        🖱️ Drag to Rotate · Scroll to Zoom
      </div>
    </div>
  );
};
