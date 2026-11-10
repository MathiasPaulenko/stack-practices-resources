# Java multi-stage: Gradle builds the jar, JRE-alpine runs it.
# Swap the runtime for gcr.io/distroless/java21-debian12 for a shell-free base.
FROM gradle:8-jdk21 AS builder

WORKDIR /app
COPY settings.gradle build.gradle ./
COPY src ./src
RUN gradle bootJar --no-daemon

FROM eclipse-temurin:21-jre-alpine

RUN addgroup -S appgroup && adduser -S appuser -G appgroup
COPY --from=builder /app/build/libs/*.jar /app/app.jar

USER appuser
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
