// Expedia-Style Authentication Frontend Implementation Example

class ExpediaAuth {
    constructor(baseUrl = 'http://127.0.0.1:8000') {
        this.baseUrl = baseUrl;
        this.staticOTP = '123456'; // For development only
    }

    // === SIGNUP FLOW ===
    
    async sendSignupOTP(email, phone = null) {
        /*
        Step 1: Send OTP for new user signup
        
        Frontend UI:
        - User enters email (required)
        - User enters phone (optional)
        - Show "Send OTP" button
        */
        
        try {
            const response = await fetch(`${this.baseUrl}/auth/signup/send-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    email: email,
                    phone: phone 
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log('✅ OTP sent for signup:', data.message);
                console.log('🔑 OTP Code (Dev):', data.otp_code);
                return { success: true, data };
            } else {
                console.error('❌ Signup OTP error:', data.detail);
                return { success: false, error: data.detail };
            }
        } catch (error) {
            console.error('❌ Network error:', error);
            return { success: false, error: 'Network error' };
        }
    }
    
    async completeSignup(email, username, password, otpCode) {
        /*
        Step 2: Complete signup with OTP verification
        
        Frontend UI:
        - Show OTP input field
        - Show username/password fields
        - Show "Complete Signup" button
        */
        
        try {
            const response = await fetch(`${this.baseUrl}/auth/signup/complete`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: email,
                    username: username,
                    password: password,
                    otp_code: otpCode
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log('✅ Signup completed:', data);
                localStorage.setItem('user', JSON.stringify(data));
                return { success: true, user: data };
            } else {
                console.error('❌ Signup completion error:', data.detail);
                return { success: false, error: data.detail };
            }
        } catch (error) {
            console.error('❌ Network error:', error);
            return { success: false, error: 'Network error' };
        }
    }

    // === LOGIN FLOW ===
    
    async sendLoginOTP(email) {
        /*
        Step 1: Send OTP for existing user login
        
        Frontend UI:
        - User enters email
        - Show "Send OTP" button
        */
        
        try {
            const response = await fetch(`${this.baseUrl}/auth/login/send-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log('✅ OTP sent for login:', data.message);
                console.log('🔑 OTP Code (Dev):', data.otp_code);
                return { success: true, data };
            } else {
                console.error('❌ Login OTP error:', data.detail);
                return { success: false, error: data.detail };
            }
        } catch (error) {
            console.error('❌ Network error:', error);
            return { success: false, error: 'Network error' };
        }
    }
    
    async verifyLoginOTP(email, otpCode) {
        /*
        Step 2: Login with OTP verification
        
        Frontend UI:
        - Show OTP input field
        - Show "Login" button
        */
        
        try {
            const response = await fetch(`${this.baseUrl}/auth/login/verify-otp`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    email: email,
                    otp_code: otpCode
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                console.log('✅ Login successful:', data);
                localStorage.setItem('authToken', data.token);
                localStorage.setItem('user', JSON.stringify(data.user));
                return { success: true, data };
            } else {
                console.error('❌ Login verification error:', data.detail);
                return { success: false, error: data.detail };
            }
        } catch (error) {
            console.error('❌ Network error:', error);
            return { success: false, error: 'Network error' };
        }
    }

    // === UTILITY METHODS ===
    
    getCurrentUser() {
        const user = localStorage.getItem('user');
        return user ? JSON.parse(user) : null;
    }
    
    getAuthToken() {
        return localStorage.getItem('authToken');
    }
    
    logout() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        console.log('✅ Logged out successfully');
    }
    
    isLoggedIn() {
        return this.getAuthToken() !== null;
    }
}

// === USAGE EXAMPLE ===

/*
// Initialize auth system
const auth = new ExpediaAuth();

// Signup Flow Example
async function handleSignup() {
    const email = 'user@example.com';
    const phone = '+1234567890';
    
    // Step 1: Send OTP
    const otpResult = await auth.sendSignupOTP(email, phone);
    if (otpResult.success) {
        // Show OTP input form
        const otpCode = '123456'; // User enters this
        const username = 'johndoe';
        const password = 'password123';
        
        // Step 2: Complete signup
        const signupResult = await auth.completeSignup(email, username, password, otpCode);
        if (signupResult.success) {
            console.log('User signed up:', signupResult.user);
            // Redirect to dashboard
        }
    }
}

// Login Flow Example
async function handleLogin() {
    const email = 'user@example.com';
    
    // Step 1: Send OTP
    const otpResult = await auth.sendLoginOTP(email);
    if (otpResult.success) {
        // Show OTP input form
        const otpCode = '123456'; // User enters this
        
        // Step 2: Verify OTP and login
        const loginResult = await auth.verifyLoginOTP(email, otpCode);
        if (loginResult.success) {
            console.log('User logged in:', loginResult.data.user);
            // Redirect to dashboard
        }
    }
}
*/

export default ExpediaAuth;
