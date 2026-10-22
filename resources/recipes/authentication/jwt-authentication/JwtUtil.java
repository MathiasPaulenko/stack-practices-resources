import io.jsonwebtoken.Claims;
import io.jsonwebtoken.ExpiredJwtException;
import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import java.nio.charset.StandardCharsets;
import java.util.Date;
import javax.crypto.SecretKey;

/**
 * Minimal JWT sign/verify for JJWT 0.12+.
 *
 * Dependencies (Maven):
 *   io.jsonwebtoken:jjwt-api:0.12.6
 *   io.jsonwebtoken:jjwt-impl:0.12.6   (runtime)
 *   io.jsonwebtoken:jjwt-jackson:0.12.6 (runtime)
 *
 * Compiling against the deprecated 0.9.x API (SignatureAlgorithm,
 * setSigningKey) will break on 0.11+ — always derive a SecretKey with
 * Keys.hmacShaKeyFor and use verifyWith()/parseSignedClaims().
 */
public class JwtUtil {

    private static final SecretKey KEY =
        Keys.hmacShaKeyFor(System.getenv("JWT_SECRET").getBytes(StandardCharsets.UTF_8));
    private static final long ACCESS_TTL = 15 * 60 * 1000L; // 15 min

    public String createToken(String userId) {
        Date now = new Date();
        return Jwts.builder()
            .subject(userId)
            .issuedAt(now)
            .expiration(new Date(now.getTime() + ACCESS_TTL))
            .signWith(KEY)
            .compact();
    }

    public Claims verifyToken(String token) {
        try {
            return Jwts.parser()
                .verifyWith(KEY)
                .build()
                .parseSignedClaims(token)
                .getPayload();
        } catch (ExpiredJwtException e) {
            throw new IllegalArgumentException("Token has expired");
        } catch (JwtException e) {
            throw new IllegalArgumentException("Invalid token");
        }
    }

    public static void main(String[] args) {
        JwtUtil util = new JwtUtil();
        String token = util.createToken("user-123");
        Claims claims = util.verifyToken(token);
        System.out.println("access token ok, sub = " + claims.getSubject());
    }
}
