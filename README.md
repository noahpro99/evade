![EVADE Logo](frontend/public/name.png)

# EVADE

Proactive personal safety through AI-powered smart glasses

## Inspiration

Walking home late at night, waiting at a bus stop, or sending kids off to school, safety is always in the back of people’s minds. Yet the tools we rely on today are reactive. Registries exist, but they only help if you search them. Parents often worry about strangers, but most decisions are based on gut feelings that can be wrong. We wanted to flip the script. Instead of reacting after something happens, what if technology could quietly stand guard and warn us before danger strikes? That idea became EVADE.

## What it does

EVADE is a personal guardian you wear on your face.

- **Adult Mode**: While wearing Meta smart glasses, EVADE scans the crowd around you. If someone matches a registered sex offender, you get an instant alert with their photo, conviction history, and risk level.
- **Kid Mode**: In addition to Adult Mode features, EVADE listens to the last 30 seconds of conversation and looks for warning signs of danger or grooming. If something feels off, parents get a notification right away with context and location.

EVADE replaces fear and bias with real information and creates a safety net that can even extend to Amber Alerts, detecting missing people.

## How we built it

- **Hardware**: Meta Ray-Ban smart glasses capture live video and audio, acting as the eyes and ears of EVADE.
- **Vision AI**: We used Mediapipe for fast on-device face detection and ArcFace for recognition. To speed up matching, we pre-embedded the entire sex offender registry into vector space for instant similarity search.
- **Audio AI (Kid Mode)**: A lightweight NLP model analyzes the last 30 seconds of conversation, detecting risky or predatory language patterns.
- **Backend**: A Python/Flask API powered by ONNXRuntime runs AI inference, updates offender data, and coordinates alerts.
- **Mobile App**: Built as a React PWA, it lets users configure modes, receive alerts, and share location data when needed.
- **Notifications**: Integrated the Instagram API to deliver real-time direct messages so guardians are notified immediately.

## Challenges we ran into

- Making face recognition fast enough to run on wearable hardware.
- Prompt engineering an AI model to catch danger in conversations without constant false alarms.
- Balancing privacy with safety — deciding what data stays on device and what gets processed in the cloud.
- Working with early, limited APIs for smart glasses.

## Accomplishments that we're proud of

- Built a working prototype that recognizes offenders in real time.
- Proved we could analyze live conversations and flag danger for kids.
- Designed an end-to-end system: glasses → AI → mobile app → instant alert.
- Took a bold idea — proactive personal safety — and made it real.

## What we learned

- Building for safety means every design choice carries ethical weight, from how we store data to how we notify users.
- Optimization is critical. Running AI models in real time on wearable hardware forced us to streamline everything, from vector search to NLP inference.
- Preprocessing matters. Pre-embedding offender registries into vectors cut search times dramatically and made the system usable.
- Integrating multiple platforms — smart glasses, backend APIs, React app, and Instagram messaging — taught us how to unify very different systems into one seamless flow.

## What's next for EVADE

- Expand Kid Mode to better detect grooming, manipulation, and distress signals.
- Integrate Amber Alerts so the community can help locate missing children faster.
- Refine on-device AI for faster, more private processing.
- Pilot EVADE with parents and safety groups to gather real-world feedback.

## Try it out

```bash
uv sync --extra cpu # or uv sync --extra cu129 for GPU
uv run src/main.py
```
