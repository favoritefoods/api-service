FROM python:3.7 AS builder

WORKDIR /usr/src/app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

RUN pip install --upgrade pip

COPY . .
# installs extra? packages (contains the openapi-server package for running the api though)
RUN pip install --no-cache-dir .
# installs missing pynamodb and other packages not included above
RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.7 AS test_runner
WORKDIR /tmp
COPY --from=builder /venv /venv
COPY --from=builder /usr/src/app/tests tests
ENV PATH=/venv/bin:$PATH

# install test dependencies
# RUN pip install pytest

# run tests
# RUN pytest tests


FROM python:3.7 AS service
WORKDIR /root/app/site-packages
COPY --from=test_runner /venv /venv
ENV PATH=/venv/bin:$PATH
