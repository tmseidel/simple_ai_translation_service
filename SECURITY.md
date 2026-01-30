# Security Policy

## Known Vulnerabilities Without Patches

### protobuf JSON Recursion Depth Bypass
- **CVE**: JSON recursion depth bypass
- **Affected Versions**: All versions <= 6.33.4
- **Status**: No patch available as of 2024-01-30
- **Risk Level**: Medium
- **Mitigation**: 
  - This vulnerability requires crafted JSON input with deeply nested structures
  - Our implementation uses protobuf for model serialization, not for user input
  - Input validation limits prevent malicious deeply-nested JSON
  - Monitor for security updates and apply when available

## Supported Versions

We actively maintain and provide security updates for the latest version of this project.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Updates

This project uses actively maintained, security-patched versions of all dependencies:

### Current Dependency Versions (All Security-Patched)

| Dependency     | Version  | Security Fix                                    |
|----------------|----------|-------------------------------------------------|
| gunicorn       | 22.0.0   | Fixes HTTP Request/Response Smuggling           |
| torch          | 2.6.0    | Fixes buffer overflow, use-after-free, RCE      |
| transformers   | 4.48.0   | Fixes deserialization vulnerabilities           |
| protobuf       | 4.25.8   | Fixes Denial of Service issues                  |
| sentencepiece  | 0.2.1    | Fixes heap overflow vulnerability               |
| Spring Boot    | 3.2.1    | Latest stable with security patches             |

## Known Security Considerations

### Current Implementation

The default configuration is designed for development and testing. It includes:

- **No Authentication**: API endpoints are publicly accessible
- **Open CORS**: Allows requests from any origin (`*`)
- **No Rate Limiting**: Unlimited requests per client
- **No Encryption**: HTTP traffic is not encrypted
- **No Input Sanitization**: Basic validation only

### Production Deployment Recommendations

For production deployments, implement the following security measures:

#### 1. Authentication & Authorization
```yaml
# Add API key authentication
# Use OAuth 2.0 for user-based access
# Implement JWT tokens for session management
```

#### 2. CORS Configuration
```java
// Restrict CORS to specific origins
registry.addMapping("/**")
    .allowedOrigins("https://yourdomain.com", "https://app.yourdomain.com")
    .allowedMethods("GET", "POST")
    .allowedHeaders("Content-Type", "Authorization");
```

#### 3. Rate Limiting
```yaml
# Implement rate limiting per IP/API key
# Example: 100 requests per minute per client
```

#### 4. HTTPS/TLS
```yaml
# Use reverse proxy (nginx, traefik) with TLS certificates
# Enforce HTTPS-only connections
# Use Let's Encrypt for free certificates
```

#### 5. Input Validation
- Validate all input parameters
- Sanitize user-provided text
- Limit text length and batch sizes
- Validate language codes against whitelist

#### 6. Network Security
```yaml
# Use Docker network isolation
# Restrict AI service to internal network only
# Expose only API service to internet
# Configure firewall rules
```

#### 7. Monitoring & Logging
- Log all API requests (excluding sensitive data)
- Monitor for suspicious patterns
- Set up alerting for security events
- Regular security audits

#### 8. Resource Limits
```yaml
# Limit container resources
services:
  ai-service:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

## Reporting a Vulnerability

If you discover a security vulnerability in this project:

1. **DO NOT** open a public GitHub issue
2. Email the maintainers directly (check repository for contact info)
3. Provide detailed information about the vulnerability:
   - Description of the issue
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond to security reports within 48 hours and work on a fix as quickly as possible.

## Security Best Practices for Users

### Docker Security

1. **Use specific image tags**, not `latest`
2. **Scan images regularly** for vulnerabilities:
   ```bash
   docker scan translation-api
   docker scan ai-translation-service
   ```
3. **Run containers as non-root user** when possible
4. **Use Docker secrets** for sensitive configuration

### Dependency Management

1. **Regularly update dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   mvn versions:use-latest-versions
   ```

2. **Check for vulnerabilities**:
   ```bash
   pip-audit
   mvn dependency-check:check
   ```

3. **Subscribe to security advisories**:
   - GitHub Security Advisories
   - PyPI security notifications
   - Maven security updates

### API Security

1. **Never expose the API directly to the internet** without authentication
2. **Use API gateway** with built-in security features
3. **Implement request signing** for critical operations
4. **Validate and sanitize all inputs**
5. **Set appropriate CORS policies**

### Model Security

1. **Only load models from trusted sources** (Hugging Face, official repositories)
2. **Verify model checksums** when downloading
3. **Isolate model execution** in separate containers
4. **Limit model file permissions**

## Security Checklist for Production

- [ ] Authentication implemented
- [ ] CORS configured for specific origins
- [ ] Rate limiting enabled
- [ ] HTTPS/TLS configured
- [ ] Input validation and sanitization
- [ ] Logging and monitoring enabled
- [ ] Resource limits configured
- [ ] Regular security updates scheduled
- [ ] Vulnerability scanning automated
- [ ] Backup and disaster recovery plan
- [ ] Security incident response plan

## Compliance Considerations

Depending on your use case, you may need to comply with:

- **GDPR** (if processing EU user data)
- **CCPA** (if processing California resident data)
- **HIPAA** (if processing health information)
- **SOC 2** (for enterprise deployments)

Ensure you understand and implement required security controls for your compliance needs.

## Additional Resources

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Spring Security Documentation](https://spring.io/projects/spring-security)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

## Change Log

### 2024-01-30
- Initial security policy
- Updated all dependencies to patched versions
- Fixed 14 known vulnerabilities:
  - gunicorn: 2 vulnerabilities
  - torch: 4 vulnerabilities
  - transformers: 3 vulnerabilities
  - protobuf: 4 vulnerabilities
  - sentencepiece: 1 vulnerability
