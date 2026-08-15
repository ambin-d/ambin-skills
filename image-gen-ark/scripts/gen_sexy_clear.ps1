$key = "ark-97ba4ce2-9565-48b1-827d-63852e913ced-58065"
$prompt = "Fashion character design sheet of a modern young Asian woman, ultra-realistic photographic quality, cinematic lighting, moody film-like atmosphere, professional portrait photography, clean light-gray studio background. Left side: head-and-shoulders front close-up of an elegant young Asian woman with delicate oval face, almond eyes, soft refined features, clean ethereal makeup, clear sharp facial details, visible skin texture. Right side: three full-body views (front, side, back), razor sharp, ultra clear, crisp outlines, no blur, showing the complete outfit structure. Tall slender figure with graceful curves, full bust, small perky butt, long slim legs. Sexy elegant outfit: fitted black lace-trimmed slip dress showing neckline and shoulders. Hair: dark brown long wavy hair. Subject: young Asian woman, fair cool-toned skin, cold elegant aloof temperament, serene noble expression. 16:9."
$models = @("doubao-seedream-4-0-250828","doubao-seedream-4-0","doubao-seedream-2-1","doubao-seedream-3-0-t2i-250415","doubao-seedream-3-0-t2i-250828","doubao-seedream-4-0-260615")
foreach ($m in $models) {
  try {
    $body = @{ model = $m; prompt = $prompt; size = "1280x720"; response_format = "url" } | ConvertTo-Json
    $r = Invoke-RestMethod -Uri "https://ark.cn-beijing.volces.com/api/v3/images/generations" -Method Post -Headers @{ "Authorization" = "Bearer $key" } -ContentType "application/json" -Body $body
    Write-Output ("OK_MODEL=" + $m)
    Write-Output $r.data[0].url
    break
  } catch {
    Write-Output ("FAIL_MODEL=" + $m)
  }
}
