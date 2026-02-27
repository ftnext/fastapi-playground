# https://github.com/open-telemetry/opentelemetry-ruby-contrib/blob/1c6c7e27577de8310997e1906fcfe4636d917870/instrumentation/faraday/example/faraday.rb
require 'bundler/setup'

Bundler.require

ENV['OTEL_TRACES_EXPORTER'] = 'console'
OpenTelemetry::SDK.configure do |c|
  c.use 'OpenTelemetry::Instrumentation::Faraday'
end

conn = Faraday.new('http://localhost:8000')
conn.get('/')
