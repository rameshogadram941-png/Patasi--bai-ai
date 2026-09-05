{{/* Helper templates */}}
{{- define "patasi-bai-ai.name" -}}
patasi-bai-ai
{{- end -}}

{{- define "patasi-bai-ai.fullname" -}}
{{ include "patasi-bai-ai.name" . }}
{{- end -}}
