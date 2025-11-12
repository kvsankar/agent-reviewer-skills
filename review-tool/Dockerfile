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

# Install Claude Code CLI (provides 'claude' command for OAuth authentication)
RUN npm install -g @anthropic-ai/claude-code

# Install uv package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy review tool only (skills will be mounted as volume)
COPY review-tool/ /app/

# Install Python dependencies
# Only Claude provider is supported
RUN uv pip install --system python-dotenv pyyaml anthropic

# Create app directory - reviews will be mounted as volume
RUN mkdir -p /app

# Create a non-root user to run the application
RUN useradd -m -u 1000 appuser && \
    mkdir -p /home/appuser/.claude && \
    chown -R appuser:appuser /home/appuser/.claude
USER appuser

# Reviews directory will be mounted from host with correct permissions
WORKDIR /app

# Set entrypoint to review script
ENTRYPOINT ["python", "review.py"]

# Default command shows help
CMD ["--help"]
