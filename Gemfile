source "https://rubygems.org"
ruby RUBY_VERSION

# Hello! This is where you manage which Jekyll version is used to run.
# When you want to use a different version, change it below, save the
# file and run `bundle install`. Run Jekyll with `bundle exec`, like so:
#
#     bundle exec jekyll serve
#
# This will help ensure the proper Jekyll version is running.
# Happy Jekylling!
gem "jekyll", "~> 3.10"
# Gems removed from the Ruby stdlib in 3.4/4.0 that Jekyll 3.x deps still require
gem "csv"
gem "webrick"
gem "base64"
gem "bigdecimal"
gem "logger"
gem "ostruct"
gem "benchmark"
gem "drb"
gem "mutex_m"

# This is the default theme for new Jekyll sites. You may change this to anything you like.
gem "minima", "~> 2.0"
gem "jekyll-theme-midnight"

# kramdown 2.x split the GFM parser into its own gem; GitHub Pages uses GFM input
gem "kramdown-parser-gfm"
gem "faraday-retry" # silences an octokit/jekyll-gist warning

# If you want to use GitHub Pages, remove the "gem "jekyll"" above and
# uncomment the line below. To upgrade, run `bundle update github-pages`.
# gem "github-pages", "~> 204", group: :jekyll_plugins
# github-pages pins liquid 4.0.3, which calls Object#tainted? (removed in Ruby 3.2).
# GitHub builds this site server-side with its own gems, so it is not needed locally.
# gem 'github-pages', group: :jekyll_plugins

# If you have any plugins, put them here!
group :jekyll_plugins do
   gem "jekyll-feed", "~> 0.6"
   gem "jekyll-paginate"
   gem "jekyll-sitemap"
   gem "jekyll-gist"
#   gem "jekyll-lunr-js-search"
end

# Windows does not include zoneinfo files, so bundle the tzinfo-data gem
gem 'tzinfo-data', platforms: [:windows, :jruby]
