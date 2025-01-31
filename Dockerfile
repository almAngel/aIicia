FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-runtime

WORKDIR /app

COPY ./aIicia /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "transcript.py"]