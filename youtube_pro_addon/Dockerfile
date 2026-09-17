ARG BUILD_ARCH=amd64
FROM ghcr.io/home-assistant/${BUILD_ARCH}-base:3.22
RUN apk add --no-cache python3 py3-pip deno
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages
COPY . .
RUN chmod a+x run.sh && sed -i 's/\r$//' run.sh
CMD [ "./run.sh" ]
