# Build em Java 25; os testes da aplicação são executados pela CI.
FROM eclipse-temurin:25-jdk AS build
WORKDIR /app
COPY .mvn/ .mvn/
COPY mvnw pom.xml ./
RUN sed -i 's/\r$//' mvnw && chmod +x mvnw
COPY src/ src/
RUN ./mvnw --batch-mode -DskipTests package

FROM eclipse-temurin:25-jre AS runtime
WORKDIR /app
RUN useradd --system --uid 10001 --no-create-home app
COPY --from=build --chown=app:app /app/target/*.jar /app/app.jar
USER app
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
