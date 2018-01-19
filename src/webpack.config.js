var path = require('path')
var webpack = require('webpack')
var HtmlWebpackPlugin = require('html-webpack-plugin')
var HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin')
var WebpackCleanPlugin = require('webpack-clean');

module.exports = {
  context: __dirname,
  // Each page gets its own bundle
  entry: {
    index: './js/index.js'
  },
  output: {
    path: path.resolve('../'),
    filename: "[name].js",
  },
  devtool: 'inline-source-map',
  plugins: [
    new HtmlWebpackPlugin({
      filename:'index.html',
      template:'./html/index.html',
      inlineSource: '.(js|css)$',
    }),
    new HtmlWebpackInlineSourcePlugin(),
    new WebpackCleanPlugin([
      '../index.js',
    ])
  ],

  module: {
    rules: [
      {
        test: /\.jsx?$/,
        // chartbuilder and included modules need their jsx compiled, but most node-modules do not
        exclude: /node_modules(?!([\\]+|\/)(react-tangle|chartbuilder))/,
        loader: 'babel-loader',
        query: {presets: ['env', 'react']}  // to transform JSX into JS
      },
      {
        test: /\.css$/,
        use: [{
          loader: 'style-loader'
        }, {
          loader: 'css-loader'
        }]
      }
    ]
  },

  resolve: {
    modules: ['node_modules', 'chartbuilder'],
    extensions: ['.js', '.jsx']
  },
}
