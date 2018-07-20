<?php

class HelloStream
{
    protected $position;
    protected $code;

    public function stream_open($path, $mode, $options, &$opened_path)
    {
        $url = parse_url($path);
        $name = $url["host"];
        $this->code = "<?php echo 'hello, {$name}';";
        $this->position = 0;
        return true;
    }

    public function stream_read($count)
    {
        $ret = substr($this->code, $this->position, $count);
        $this->position += strlen($ret);
        return $ret;
    }

    public function stream_tell()
    {
        return $this->position;
    }

    public function stream_eof()
    {
        return $this->position >= strlen($this->code);
    }

    public function stream_seek($offset, $whence)
    {
        switch ($whence) {
            case SEEK_SET:
                if ($offset < strlen($this->code) && $offset >= 0) {
                    $this->position = $offset;
                    return true;
                } else {
                    return false;
                }
                break;

            case SEEK_CUR:
                if ($offset >= 0) {
                    $this->position += $offset;
                    return true;
                } else {
                    return false;
                }
                break;
            case SEEK_END:
                if (strlen($this->code) + $offset >= 0) {
                    $this->position = strlen($this->code) + $offset;
                    return true;
                } else {
                    return false;
                }
                break;

            default:
                return false;
        }
    }
    public function stream_stat()
    {
        return stat(__FILE__);
    }
}

stream_wrapper_register('hello', HelloStream::class);
include 'hello://dxkite';
