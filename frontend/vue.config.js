module.exports = {
    productionSourceMap: false,
    publicPath: process.env.VUE_APP_PUBLIC_ROOT_PATH,
    chainWebpack: config => {
        config
          .plugin('html')
          .tap(args => {
          args[0].title = 'CommentSearch';
          return args;
        });
      }
}