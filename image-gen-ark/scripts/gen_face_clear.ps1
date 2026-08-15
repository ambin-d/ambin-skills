$key = "ark-97ba4ce2-9565-48b1-827d-63852e913ced-58065"
$prompt = @"
Fashion character design sheet of a modern young Asian woman, ultra-realistic photographic quality, cinematic lighting, professional portrait photography, clean light-gray studio background. Left side: head-and-shoulders front close-up of an elegant young Asian woman with delicate oval face, almond eyes, razor-sharp facial details, clean ethereal makeup, light pink lip color, delicate earrings, necklace, hair accessories and detailed neckline. Right side: three clear full-body views (front, side, back) showing the complete outfit structure; every figure's face is rendered in sharp focus with clearly visible, detailed facial features, no blur. Sexy outfit: black off-shoulder fitted dress with plunging neckline. Body: tall slender figure with long legs, curvy figure with fuller bust and soft feminine curves, subtle perky buttocks not exaggerated. Hair: long straight dark hair. Subject: young Asian woman, fair cool-toned skin, calm cool-gentle temperament with a hint of distance, serene noble expression. 16:9.
"@
$body = @{
    model = "doubao-seedream-4-0-250828"
    prompt = $prompt
    size = "1280x720"
    response_format = "url"
} | ConvertTo-Json -Depth 5
$headers = @{ "Authorization" = "Bearer $key"; "Content-Type" = "application/json" }
$resp = Invoke-RestMethod -Uri "https://ark.cn-beijing.volces.com/api/v3/images/generations" -Method Post -Headers $headers -Body $body
$resp.data[0].url
