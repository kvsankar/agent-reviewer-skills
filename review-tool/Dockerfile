# Claude Code Skills Review Tool - Container for Agentic Mode
#
# This container provides a safe, isolated environment for agentic code reviews
# where Claude can explore repositories using bash commands with dangerous mode enabled.
#
# Build from parent directory:
#   docker build -f review-tool/Dockerfile -t claude-reviewer .
#
# Run:
#   docker run --rm \
#     -v $(pwd)/reviews:/app/reviews \
#     -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
#     claude-reviewer \
#     --repo https://github.com/user/repo \
#     --reviewer python \
#     --agentic

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    # Indicate we're in a container for auto-detection
    IN_CONTAINER=true

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Claude CLI (for OAuth authentication)
RUN npm install -g @anthropic-ai/claude-cli

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy all skills from parent directory (build context is claude-skills-public/)
COPY *-reviewer/ /skills/

# Copy review tool
COPY review-tool/ /app/

# Install Python dependencies
# Install all providers by default in the container
RUN uv pip install --system python-dotenv pyyaml anthropic openai google-generativeai

# Create directories
RUN mkdir -p /app/reviews /root/.claude

# Set entrypoint to review script
ENTRYPOINT ["python", "review.py"]

# Default command shows help
CMD ["--help"]
