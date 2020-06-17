let fs = require('fs');
const path = require('path');
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const WorkboxPlugin = require('workbox-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
let app = require('./package.json');
let development = false;

module.exports = (env, options) => {
	console.log('================================================\n');
	console.log(`This is the Webpack 4 'mode': ${options.mode}`);
	development = options.mode != 'production';
	if (!development) {
		let v1 = parseInt(app.version.split('.')[0]);
		let v2 = parseInt(app.version.split('.')[1]);
		let v3 = parseInt(app.version.split('.')[2]);
		if (options.fix) {
			v3++;
		} else {
			v2++;
			v3 = 0;
		}
		if (v2 == 100) {
			v2 = 0;
			v1++;
		}
		app.version = `${v1}.${v2}.${v3}`;
		fs.writeFileSync(__dirname + '/package.json', JSON.stringify(app, null, 4));
		console.log(`----------- Updated version ✅ ${app.version} -----------`);
	}
	console.log('\n================================================\n');

	let babelLoader = {
		loader: 'babel-loader',
		options: {
			plugins: [
				'@babel/plugin-syntax-dynamic-import',
				'@babel/plugin-syntax-import-meta',
				'@babel/plugin-proposal-optional-chaining',
				'@babel/plugin-proposal-nullish-coalescing-operator',
				'@babel/plugin-transform-runtime',
				'@babel/plugin-transform-async-to-generator',
				[
					'template-html-minifier',
					{
						modules: {
							'lit-html': ['html'],
							'lit-element': ['html', { name: 'css', encapsulation: 'style' }],
							'@conectate/ct-lit/ct-lit': ['html', { name: 'css', encapsulation: 'style' }],
							'@c2_comp/c2-element/c2-element': ['html', { name: 'css', encapsulation: 'style' }],
							'@polymer/polymer/lib/utils/html-tag.js': ['html', { name: 'css', encapsulation: 'style' }]
						},
						htmlMinifier: {
							collapseWhitespace: true,
							removeComments: true,
							caseSensitive: true,
							minifyCSS: true
						}
					}
				],
				// webpack does not support import.meta.url yet, so we rewrite them in babel
				['bundled-import-meta', { importStyle: 'baseURI' }]
			],
			presets: [['@babel/preset-env', { targets: { chrome: development ? '80' : '49' } }]]
		}
	};
	return {
		entry: {
			app: './web/src/usac-app.ts'
		},
		output: {
			filename: '[name].bundle.js',
			chunkFilename: `[name].[chunkhash].js`,
			path: path.resolve(__dirname, 'web/dist')
		},
		devtool: development ? 'source-map' : false,
		resolve: {
			// Add '.ts' and '.tsx' as resolvable extensions.
			extensions: ['.ts', '.js', '.json'],
			alias: {
				'chart.js': 'chart.js/dist/Chart.js',
				moment: 'dayjs'
			}
		},
		plugins: [
			new webpack.DefinePlugin({
				'process.env.NODE_ENV': JSON.stringify(development ? 'dev' : 'production')
			}),
			!development && new CleanWebpackPlugin(),
			new HtmlWebpackPlugin({
				template: './web/index.html',
				minify: {
					collapseWhitespace: true,
					removeComments: true,
					caseSensitive: true,
					minifyCSS: true
				}
			}),
			new CopyPlugin([{ from: 'web/static', to: 'static' }])
		].filter(_ => !!_),
		optimization: {
			minimizer: [
				!development &&
					new TerserPlugin({
						terserOptions: {
							output: {
								comments: false
							}
						},
						parallel: true,
						sourceMap: true
					})
			].filter(_ => !!_)
		},

		module: {
			rules: [
				{
					test: /\.ts$/,
					use: [
						babelLoader,
						{
							loader: 'ts-loader',
							options: { transpileOnly: true }
						}
					]
				},
				{
					test: /\.js$/,
					use: babelLoader
				},
				{
					test: /\.svg$/,
					loader: 'svg-inline-loader'
				},
				{
					test: /\.css$/i,
					use: ['css-loader']
				}
			]
		},
		devServer: {
			writeToDisk: true,
			headers: {
				'Access-Control-Allow-Origin': '*'
			},
			disableHostCheck: true,
			contentBase: process.cwd(),
			compress: true,
			port: 8001,
			host: '0.0.0.0',
			historyApiFallback: true,
			stats: {
				stats: 'errors-only'
			},
			watchOptions: {
				ignored: [path.resolve(__dirname, 'web/static/img')]
			}
		}
	};
};
