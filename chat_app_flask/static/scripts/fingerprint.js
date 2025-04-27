// Using FingerprintJS for browser fingerprinting
async function generateFingerprint() {
    // Initialize an agent at application startup.
    const fpPromise = FingerprintJS.load();
    
    // Get the visitor identifier when you need it.
    const fp = await fpPromise;
    const result = await fp.get();

    // Return the unique identifier
    return result.visitorId;
}

export default generateFingerprint;