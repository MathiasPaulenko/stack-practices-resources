# Stage 1: Build
FROM gradle:8.7-jdk21-alpine AS builder

WORKDIR /build

COPY build.gradle settings.gradle ./
COPY src ./src

RUN gradle bootJar --no-daemon

# Stage 2: Runtime
FROM eclipse-temurin:21-jre-alpine AS runtime

WORKDIR /app

COPY --from=builder /build/build/libs/*.jar app.jar

# temurin ships no convenience user — `USER temurin` fails at runtime
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
